import os, sys
import time
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.ab_test as ab_test
import src.plan_converter as plan_converter
import src.train_yolo as train_yolo

from pathlib import Path
from queue import Queue
from datetime import datetime
import shutil

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from db.db_model_list import DbModelList
from ui.ui_model_management_widget import Ui_Widget

from dialog.add_new_model_dialog import AddNewModelDialog
from dialog.add_trained_model_dialog import AddTrainedModelDialog
from dialog.dataset_config_file_path_dialog import DatasetConfigFilePathDialog
from dialog.performance_metric_graph_dialog import PerformanceMetricGraphDialog 

from setting.use_qsetting import Setting

is_training = False

# 2025.05.21 추가 (박보은)
# 모델 학습 Q스레드
class ModelTrainQThread(QThread):
    started = Signal(int, str)
    finished = Signal(int, str, str, Path)
    error = Signal(int, str, str)
    stopped = Signal(int, str)

    def __init__(self,queue):
        super().__init__()
        self.setObjectName("ModelTrainQThread")
        
        self.process = None
        self.train_queue = queue
        
    def run(self):
        global is_training
        self.running= True
        print("########################################################################################훈련 스레드 시작")
        while self.running:
            try:
                if not self.train_queue.empty():
                    print("########################################################################################훈련 스레드 진행중")
                    self.task= self.train_queue.get()
                    is_training = True  # 훈련 작업 시작
                    self.started.emit(self.task['row'],self.task['model_name'])

                    script_path = Path(__file__).resolve().parent.parent / "src" / "train_model_process.py"  # 모델 훈련 스크립트 (.py)

                    args = [
                        "python", str(script_path),     # 실행 파일
                        self.task['model_name'],                # 모델 이름
                        self.task['dataset_config_file_path'],  # 구성 파일
                        str(self.task['retrain_flag'])          # 재훈련 여부
                    ]

                    self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
                    self.process.wait()
                    stdout, stderr = self.process.communicate()

                    if self.process.returncode == 0:
                        print("정상 종료됨!")
                        lines = stdout.strip().split('\n')
                        last_two_lines = lines[-2:]
                        values = []
                        for line in last_two_lines:
                            if ':' in line:
                                _, value = line.split(':', 1)
                                values.append(value.strip())

                        if len(values) == 2:
                            trained_model_name = values[0]
                            pt_path = values[1]
                            print(f"trained_model_name: {trained_model_name}")
                            print(f"pt_path: {pt_path}")

                            self.finished.emit(self.task['row'], self.task['model_name'], trained_model_name, Path(pt_path))
                            is_training = False  # 훈련 작업 완료
                    elif self.process.returncode == -15 or self.process.returncode == -19:
                        print("훈련 중단됨")
                        self.stopped.emit(self.task['row'], self.task['model_name'])
                        is_training = False  # 훈련 작업 중단
                    else:
                        print("오류 발생!")
                        self.error.emit(self.task['row'], self.task['model_name'], str(stdout.strip()))
                        is_training = False  # 훈련 작업 오류
                         # 오류 발생 시 대기열에서 제거
                else:
                    self.stop()
                time.sleep(0.1)
            except Exception as e:
                self.error.emit(self.task['row'], self.task['model_name'], str(e))
                is_training = False  # 훈련 작업 오류

    def is_running(self):
        return self.running
    
    def stop_train(self):
        global is_training
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)  # 최대 5초 기다림
            except subprocess.TimeoutExpired:
                print('timeout')
                self.process.kill()  # 강제 종료 (SIGKILL)
                self.process.wait()
        else:
            print("프로세스 이미 완료, 훈련 중단")
            self.stopped.emit(self.task['row'], self.task['model_name'])
            is_training = False  # 훈련 작업 중단 상태로 설정
            
    def stop(self):
        print("########################################################################################훈련 스레드 종료")
        self.running = False
        self.quit()
        self.wait()   
        
    def is_work(self):
        """현재 변환 작업이 진행 중인지 확인하는 메서드"""
        return is_training or not self.train_queue.empty()

# 레이아웃 설정 클래스
# 레이아웃 설정 클래스
class TemperaryLayout(QObject):  # QObject 상속 추가
    """레이아웃 변경을 위한 커뮤니케이션 클래스"""
    save_layout = Signal(str)  # 레이아웃 저장 신호 추가
    clear_ui = Signal()  # UI 초기화 신호 추가
    delete_layout = Signal(str)  # 레이아웃 삭제 신호 추가
    load_layout = Signal(str)  # 레이아웃 불러오기 신호 추가
    def __init__(self):
        super().__init__()  # 부모 클래스 초기화 필수
        
    def send_layout_text(self, text):
        print(f"레이아웃 텍스트 전송: {text}")
        self.save_layout.emit(text)  # 레이아웃 저장 신호 전송
    
    def load_layout_text(self, text):
        print(f"레이아웃 텍스트 불러오기: {text}")
        self.load_layout.emit(text)  
    def clear_layout(self):
        self.clear_ui.emit()  # UI 초기화 신호 전송
    def delete_layout_text(self, text):
        self.delete_layout.emit(text)
    
        
# 2025.05.21 추가 (박보은)
# pt → onnx → plan 파일 변환 Q스레드
class PtToPlanConverterQThread(QThread):
    finished = Signal(int, str, str, str,bool)
    error = Signal(int, str, str, str)
    confirm_conversion = Signal(int, str, dict)  # 확인 대화상자 표시 신호 추가
    cancel=Signal(int)  # 취소 신호 추가

    def __init__(self, queue, temperary_layout: TemperaryLayout, background_controller=None):
        super().__init__()
        self.convert_queue = queue
        self.is_converting = False  # 변환 작업 상태 추적 플래그 추가
        self.conversion_confirmed = None  # 변환 작업에 대한 사용자 응답 저장
        self.temperary_layout =temperary_layout  # 레이아웃 커뮤니케이션 객체 생성
        self.background_controller=background_controller
        self.done= False  # 변환 작업 완료 플래그

    def run(self):
        try:
            self.running = True
            print("########################################################################################변환 스레드 시작")
            while self.running:
                if not self.convert_queue.empty():
                    
                    print("########################################################################################변환 스레드 진행중")
                    task = self.convert_queue.get()
                    if self.conversion_confirmed is None:
                        self.confirm_conversion.emit(task['row'], task['trained_model_name'], task)
                        self.temperary_layout.send_layout_text("model")  # 레이아웃 저장 신호 전송
                        # 이 시점에서는 스레드가 일시 중단됨 (사용자 응답 대기)
                        # conversion_response 메서드가 호출될 때까지 기다림
                        self.wait_for_confirmation()
                    if self.conversion_confirmed :
                        if not self.done:
                            self.temperary_layout.clear_layout()  # UI 초기화 신호 전송
                            self.background_controller.stop_all_processes()  # 배경 설정
                            # self.background_controller.disconnect()
                        
                        self.is_converting = True  # 변환 작업 시작
                        plan_path = self.convert_to_plan(task['row'], task['trained_model_name'], task['pt_path'])
                        self.finished.emit(task['row'], task['based_model_name'], task['trained_model_name'], plan_path,self.done)
                        self.is_converting = False  # 변환 작업 완료
                        self.done = True  # 변환 작업 완료 상태로 설정
                    else:
                        # 사용자가 취소한 경우
                        self.stop()
                        self.temperary_layout.delete_layout_text("model")  # UI 초기화 신호 전송
                        self.cancel.emit(task['row'])
                        
                else:
                    self.stop()
                time.sleep(0.1)
        except Exception as e:
            self.is_converting = False  # 예외 발생 시에도 변환 작업 상태 업데이트
            self.done = False  # 변환 작업 완료 상태 초기화
            self.error.emit(task['row'], task['based_model_name'], task['trained_model_name'], str(e))
            self.temperary_layout.delete_layout_text("model")  # 레이아웃 삭제 신호 전송
            return
        
    def wait_for_confirmation(self):
        # 사용자 응답을 기다리는 메서드
        # 이벤트 루프를 사용하여 대기
        loop = QEventLoop()
        self.confirmation_loop = loop
        loop.exec()      
        
    def set_conversion_response(self, confirmed, task):
        # 사용자 응답에 따라 처리
        self.conversion_confirmed = confirmed
        if confirmed:
            self.task = task
        # 대기 중인 이벤트 루프 종료
        if hasattr(self, 'confirmation_loop') and self.confirmation_loop.isRunning():
            self.confirmation_loop.quit()  
               
    def convert_to_plan(self, row, trained_model_name, pt_path):
            time.sleep(3)
            plan_path = plan_converter.main(trained_model_name, pt_path)
            return plan_path

    def is_running(self):
        return self.running
    
    def is_work(self):
        """현재 변환 작업이 진행 중인지 확인하는 메서드"""
        return self.is_converting or not self.convert_queue.empty()

    def stop(self):
        print("########################################################################################변환 스레드 종료")
        self.running = False
        self.conversion_confirmed = None  # 변환 작업 상태 초기화
        if self.done:
            self.background_controller.start_all_processes()  # 배경 설정
            self.background_controller.connect()
            time.sleep(5)  # 배경 설정 후 잠시 대기
            self.temperary_layout.load_layout_text("model")  # 레이아웃 불러오기 신호 전송
            time.sleep(1)  # 레이아웃 불러오기 신호 전송 후 잠시 대기
            self.temperary_layout.delete_layout_text("model")  # 레이아웃 삭제 신호 전송
            
        self.done = False  # 변환 작업 완료 상태 초기화
        self.quit()
        self.wait()
# 2025.05.21 추가 (박보은)
# Triton 서버 내 모델 업로드 Q스레드
class ModelUploadQThread(QThread):
    finished = Signal(int, str, str, str)
    error = Signal(int, str, str, str)

    def __init__(self, row, based_model_name, trained_model_name, plan_path):
        super().__init__()
        self.setObjectName("ModelUploadQThread")
        self.row = row
        self.based_model_name = based_model_name
        self.trained_model_name = trained_model_name
        self.plan_path = plan_path
        print(f'row: {row}, trained_model_name: {trained_model_name}, plan_path: {plan_path}')

    def run(self):
        try:
            curl_command = [
                "curl", 
                "-X", "POST", 
                f"http://[::1]:8000/v2/repository/models/{self.trained_model_name}/load"
            ]

            result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
            print(result)
            # curl 실행 결과 처리
            if result.returncode != 0 or '"error"' in result.stdout:
                self.error.emit(self.row, self.based_model_name, self.trained_model_name, result.stderr)
            else:
                self.finished.emit(self.row, self.based_model_name, self.trained_model_name, self.plan_path)

        except subprocess.CalledProcessError as e:
            self.error.emit(self.row, self.based_model_name, self.trained_model_name, str(e))
        except Exception as e:
            print(f"오류 발생: {e}")
            self.error.emit(self.row, self.based_model_name, self.trained_model_name, str(e))

# 2025.05.21 추가 (박보은)
# 성능 평가 Q스레드
class PerformanceEvaluationQThread(QThread):
    started = Signal(int)
    finished = Signal(int, str, dict)
    error = Signal(int, str, str)

    def __init__(self, row, model_name, dataset_config_file_path):
        super().__init__()
        self.setObjectName("PerformanceEvaluationQThread")
        self.row = row
        self.model_name = model_name
        self.dataset_config_file_path = dataset_config_file_path
    def run(self):
        try:
            print("!!!!!!!!!!!!!!!!!!!성능평가 스레드 시작")
            self.started.emit(self.row)
            
            perform_val = ab_test.model_performance_value('experiments', self.model_name, self.dataset_config_file_path)
            if perform_val:
                self.finished.emit(self.row, self.model_name, perform_val['Metrics'])
            else:
                self.error.emit(self.row, self.model_name, '성능평가 결과 값이 없습니다.')
        except Exception as e:
            self.error.emit(self.row, self.model_name, str(e))

# 2025.05.21 추가 (박보은)
# 테이블 셀 델리게이트
class CellButtonDelegate(QStyledItemDelegate):
    clicked = Signal(int, int)

    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.icon = QIcon(icon_path)
        # self.state = state

    def paint(self, painter, option, index):
        row, col = index.row(), index.column()
        model = index.model()
        text = model.index(row, 4).data()

        # 1열 (모델명)
        if col in (0, 1, 2):
            # 학습 대기 중 상태일 때는 기본 배경색 사용 (별도 색상 지정 안 함)
            if '(상태: 학습 대기 중)' in text:
                painter.fillRect(option.rect, QBrush(QColor(255, 255, 255)))
            # 학습중 # 파일변환중
            elif '[ 학습 중단 ]' in text or '[ 파일변환 취소 ]' in text:
                # 초록색
                painter.fillRect(option.rect, QBrush(QColor(150, 255, 150)))
            # 학습중단
            elif '[ 학습 이어하기 ]' in text or '학습 중단 요청 처리' in text:
                # 주황색
                painter.fillRect(option.rect, QBrush(QColor(255, 200, 100)))
            # 오류
            elif '[ 재학습 ]' in text:
                # 빨간색
                painter.fillRect(option.rect, QBrush(QColor(255, 150, 150)))
            
            super().paint(painter, option, index)
        elif col in (3, 4, 5):
            btn_option = QStyleOptionButton()
            btn_option.rect = option.rect
            btn_option.state = QStyle.State_Enabled

            if col in (4, 5):
                btn_option.text = index.data()
            else:
                btn_option.icon = self.icon
                btn_option.iconSize = option.rect.size() * 0.8  # 아이콘 크기 조정

            # 학습 대기 중 상태일 때는 기본 배경색 사용
            if '(상태: 학습 대기 중)' in text:
                # 버튼에 기본 팔레트 사용
                # print('학습 대기 중 상태')
                btn_option.palette = QApplication.style().standardPalette()
            # 학습중 # 파일변환중
            elif '[ 학습 중단 ]' in text or '[ 파일변환 취소 ]' in text:
                # 초록색
                palette = QPalette()
                palette.setColor(QPalette.Button, QColor(150, 255, 150))  # 버튼 배경
                btn_option.palette = palette
            # 학습중단
            elif '[ 학습 이어하기 ]' in text or '학습 중단 요청 처리' in text:
                # print('학습 이어하기')
                # 주황색
                palette = QPalette()
                palette.setColor(QPalette.Button, QColor(255, 200, 100))  # 버튼 배경
                btn_option.palette = palette
            # 오류
            elif '[ 재학습 ]' in text:
                # 빨간색
                palette = QPalette()
                palette.setColor(QPalette.Button, QColor(255, 150, 150))  # 버튼 배경
                btn_option.palette = palette

            QApplication.style().drawControl(QStyle.CE_PushButton, btn_option, painter)
    def editorEvent(self, event, model, option, index):
        col = index.column()
        if col in (1, 3, 4, 5) and event.type() == QEvent.MouseButtonRelease:
            if option.rect.contains(event.pos()):
                self.clicked.emit(index.row(), index.column())
        return super().editorEvent(event, model, option, index)


class ModelListManagementWidget(QDialog, Ui_Widget):
    def __init__(self,temperary_layout: TemperaryLayout,background_controller=None, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setMouseTracking(True)  # 마우스 트래킹 활성화
        
        self.dataset_config_file_path="-" # 데이터셋 구성파일 경로 기본 값
        self.settings = Setting("model_list_setting.ini")
        
        self.button_add_new_model.clicked.connect(self.on_btn_add_new_model_clicked)   # 버튼 이벤트 연결
        self.button_delete_model.clicked.connect(self.on_btn_delete_model_clicked)
        self.img_path = str(Path(__file__).resolve().parent.parent / "src/icon/graph_2.png")
        self.model_metrics_key = ['precision', 'recall', 'map50', 'map50_95', 'f1_score', 'speed']
        self.button_delegate_cell = None
        self.hidden_pending_close= False
        self.train_stopped = False
        print(f"hidden_pending_close: {self.hidden_pending_close}")
        
        self.temperary_layout = temperary_layout  # 레이아웃 설정 객체
        self.background_controller = background_controller  # 배경 컨트롤러
        
        self.db_model_list = DbModelList()
        self.upload_threads = {}
        self.performance_evaluation_threads = {}
        
        self.train_queue = Queue()
        self.train_thread = ModelTrainQThread(self.train_queue)
        self.train_thread.started.connect(self.on_model_train_started)
        self.train_thread.finished.connect(self.on_model_train_finished)
        self.train_thread.error.connect(self.on_model_train_error)
        self.train_thread.stopped.connect(self.on_model_train_stopped)
        self.train_thread.start()
        
        self.convert_queue = Queue()
        self.converter_thread = PtToPlanConverterQThread(self.convert_queue, self.temperary_layout,self.background_controller)
        self.converter_thread.finished.connect(self.on_path_convert_finished)
        self.converter_thread.error.connect(self.on_path_convert_error)
        self.converter_thread.cancel.connect(self.on_path_convert_cancel)
        self.converter_thread.confirm_conversion.connect(self.show_conversion_confirmation)
        self.converter_thread.start()
        
        self.load_model_data()  # 모델 데이터 불러오기
        
    # 데이터셋 구성파일 정보 불러오기
    def get_path_info(self, model_description):
        # Setting 클래스의 get 메서드 사용, group 인자 전달
        dataset_config_file_path = self.settings.get('dataset_config_file_path', '-', group=model_description)
        
        # 파일 존재 여부 확인은 여기서 해도 되고, 사용하는 쪽에서 해도 됩니다.
        if not dataset_config_file_path or dataset_config_file_path == '-' or not os.path.exists(dataset_config_file_path):
            # print(f"Path '{dataset_config_file_path}' is invalid or does not exist. Returning '-'")
            dataset_config_file_path = "-"
        return dataset_config_file_path

    # 데이터셋 구성파일 정보 저장
    def save_path_info(self, model_description, dataset_config_file_path):
        """경로 정보를 QSettings에 저장"""

        self.settings.set('dataset_config_file_path', dataset_config_file_path,group=model_description)


    # 모델 정보 불러오기
    def load_model_data(self):
        try:
            status_text = ["[ 학습 ]", "[ 학습 중단 ]\n(상태: 학습 진행 중)", "[ 학습 이어하기 ]\n(상태: 학습 중단)", "[ 재학습 ]\n(상태: 오류)", "[ 파일변환 취소 ]\n (상태: 학습 파일변환 중)"]

            # DB에서 모든 모델 목록 가져오기
            models = self.db_model_list.select()
            
            # model_description 기준으로 오름차순 정렬
            models.sort(key=lambda model: model.model_description)
            
            item_model = QStandardItemModel()
            item_model.setColumnCount(6)
            item_model.setHorizontalHeaderLabels(
                ["모델명", "데이터 셋 구성 파일", "등록일", "성능지표", "학습", "성능 평가"]
            )

            for row, model in enumerate(models):
                model_description = model.model_description
                dataset_config_file_path = self.get_path_info(model_description)


                status = 3 if model.status != 0 and model.status!= None else 0
                column_values = [model_description, dataset_config_file_path, f"{model.model_registered_at}", "", status_text[status], "[ 성능평가 ]"]

                for col, text in enumerate(column_values):
                    item = QStandardItem(text)
                    item.setEditable(False)
                    item.setTextAlignment(Qt.AlignCenter)
                    item_model.setItem(row, col, item)

                    self.tableview_model_list.setModel(item_model)

            header = self.tableview_model_list.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch) # 열 너비를 현재 창 크기에 맞게 균등 조정
            # TableView에 모델 연결
            self.tableview_model_list.verticalHeader().setDefaultSectionSize(60)

            self.button_delegate_cell = CellButtonDelegate(self.img_path, parent=self.tableview_model_list)
            self.tableview_model_list.setItemDelegate( self.button_delegate_cell)
            self.button_delegate_cell.clicked.connect(self.handle_cell_clicked)
        except Exception as e:
            print(f"데이터 로드 중 오류 발생: {e}")


    # 테이블 셀 클릭 이벤트
    def handle_cell_clicked(self, row, column):
        view_model = self.tableview_model_list.model()
        index = view_model.index(row, 0)
        model_description = index.data()
        db_model_list= self.db_model_list.select(model_description=model_description)[0]
        model_name= db_model_list.model_name
        dataset_config_file_path = view_model.index(row, 1).data()

        if column == 1:     # 데이터셋 경로
            dataset_config_file_path = self.get_path_info(model_description)
            dataset_config_file_path_dialog = DatasetConfigFilePathDialog(model_description, dataset_config_file_path, self)
            
            if dataset_config_file_path_dialog.exec():
                view_model.setData(view_model.index(row, 1), dataset_config_file_path_dialog.get_data_config_file_path() if dataset_config_file_path_dialog.get_data_config_file_path() else '-')
                
                # 설정 저장
                self.save_path_info(
                    model_description,
                    view_model.index(row, 1).data()
                )
        elif column == 3:   # 그래프
            # model_metrics = self.db_model_list.select(model_description=model_description)[0]
            
            if all(hasattr(db_model_list, key) and getattr(db_model_list, key) is not None for key in self.model_metrics_key):
                # 성능지표 값이 존재하는 경우 그래프 표시
                graph_dialog = PerformanceMetricGraphDialog(model_description, self)
                graph_dialog.exec()
            else:
                #성능 지표 값 중 None이 있거나, hasattr가 False인 경우
                QMessageBox.critical(self, "성능지표 확인 불가", "성능 지표 값이 없습니다.")
        elif column == 4:   # 학습
            text = view_model.index(row, 4).data()
            if text == '[ 학습 ]' or '[ 재학습 ]' in text:
                print(f"{row+1}행의 2열 값: {dataset_config_file_path}")

                if dataset_config_file_path == '-':
                    QMessageBox.critical(self, "학습 불가", "데이터 셋 구성 파일이 없습니다.")
                else:
                    self.handle_train_start_cell_clicked(row, model_name, dataset_config_file_path)
            elif '[ 학습 중단 ]' in text: 
                self.train_thread.stop_train()

                view_model.setData(view_model.index(row, 4), "(상태: 학습 중단 요청 처리중)")
                view_model.dataChanged.emit(0, 5)
            elif '[ 학습 이어하기 ]' in text:
                print(f"{row+1}행의 2열 값: {dataset_config_file_path}")

                if dataset_config_file_path == '-':
                    QMessageBox.critical(self, "학습 불가", "데이터 셋 구성 파일이 없습니다.")
                else:
                    self.handle_train_start_cell_clicked(row, model_name, dataset_config_file_path, True)

        elif column == 5:
            text = view_model.index(row, 5).data()
            if dataset_config_file_path == '-':
                QMessageBox.critical(self, "성능 평가 불가", "데이터 셋 구성 파일이 없습니다.")
            else:
                if text == '[ 성능평가 ]':
                    self.handle_performance_evaluation_cell_clicked(row, model_name, dataset_config_file_path)

    """
        모델 학습 관련 함수
        handle_train_start_cell_clicked : 모델 학습 셀 클릭 이벤트
        
        on_model_train_started : 모델 학습 Q스레드 시그널 이벤트 (started)
        on_model_train_finished : 모델 학습 Q스레드 시그널 이벤트 (finished)
        on_model_train_error : 모델 학습 Q스레드 시그널 이벤트 (error)
        on_model_train_stopped : 모델 학습 Q스레드 시그널 이벤트 (stopped)

        cleanup_train_thread : 모델 학습 Q스레드 종료
    """
    def handle_train_start_cell_clicked(self, row, model_name, dataset_config_file_path, retrain_flag=False):
        global is_training
        view_model = self.tableview_model_list.model()
        if is_training:
            view_model.setData(view_model.index(row, 4), "[ 학습 ]\n(상태: 학습 대기 중)")
            view_model.dataChanged.emit(0,5)
        self.train_queue.put({"row":row,"model_name": model_name,"dataset_config_file_path": dataset_config_file_path, "retrain_flag":retrain_flag})
        if not self.train_thread.is_running():
            self.train_thread.start()
        

    def on_model_train_started(self, row, based_model_name):
        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 학습 중단 ]\n(상태: 학습 진행 중)")
        view_model.dataChanged.emit(0, 5)

        model_description = view_model.index(row, 0).data()
        result =self.db_model_list.update(model_description=model_description,model_name=based_model_name,status=1)
        print(f'result: {result}')
        
    def on_model_train_finished(self, row, based_model_name, trained_model_name, pt_path):
        self.cleanup_train_thread(based_model_name)
        self.enqueue_convert_model(row, based_model_name, trained_model_name, pt_path)
        
        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 파일변환 취소 ]\n (상태: 학습 파일변환 중)")
        view_model.dataChanged.emit(0, 5)

        model_description = view_model.index(row, 0).data()
        result = self.db_model_list.update(model_description=model_description,model_name=based_model_name,status=4)
        print(f'result: {result}')

    def on_model_train_error(self, row, based_model_name, msg):
        print(f"based_model_name: {based_model_name}")
        self.cleanup_train_thread(based_model_name)
        QMessageBox.critical(self, "학습", f"[모델 학습 실패] {based_model_name} : {msg}")

        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 재학습 ]\n(상태: 오류)")
        view_model.dataChanged.emit(0, 5)

        model_description = view_model.index(row, 0).data()
        result = self.db_model_list.update(model_description=model_description,model_name=based_model_name,status=3)
        print(f'result: {result}')

    def on_model_train_stopped(self, row, based_model_name):
        print(f"based_model_name: {based_model_name}")
        self.cleanup_train_thread(based_model_name)
        
        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 학습 이어하기 ]\n (상태: 학습 중단)")
        view_model.dataChanged.emit(0, 5)
        self.train_stopped=True
        self.threads_running = False

        model_description = view_model.index(row, 0).data()
        result = self.db_model_list.update(model_description=model_description,model_name=based_model_name,status=2)
        print(f'result: {result}')

    def cleanup_train_thread(self, model_name):
        try:
            self.check_all_threads_finished() 
        except Exception as e:
            print(f"cleanup_train_thread error: {e}")
      
    """
        파일 변환 관련 함수
        enqueue_convert_model : 파일변환 대기열 생성 함수
        on_path_convert_finished : 파일 변환 Q스레드 시그널 이벤트 (finished)
        on_path_convert_error : 파일 변환 Q스레드 시그널 이벤트 (error)
        show_conversion_confirmation : 모델 변환 전 사용자에게 확인 요청
    """
    def show_conversion_confirmation(self, row, trained_model_name, task):
        """모델 변환 전 사용자에게 확인 요청"""
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle("모델 변환 확인")
        message_box.setText(f"모델 파일형식 변환 및 업로드를 진행하는 경우 모든 영상감지가 멈춥니다. 계속하시겠습니까?\n\n 해당 작업을 승인하는 경우  대기 중인 작업 수에 따라 소요시간이 길어질 수 있습니다.(각 파일변환 소요시간: 5분)")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)
        
        result = message_box.exec()
        
        if result == QMessageBox.Yes:
            # 사용자가 '예'를 선택한 경우
            self.converter_thread.set_conversion_response(True, task)
        else:
            # 사용자가 '아니오'를 선택한 경우
            self.converter_thread.set_conversion_response(False, task)
            
    def enqueue_convert_model(self, row, based_model_name, trained_model_name, pt_path):
        self.convert_queue.put({'row':row, 'based_model_name':based_model_name, 'trained_model_name':trained_model_name, 'pt_path':pt_path})
        if not self.converter_thread.is_running():
            self.converter_thread.start()

    def on_path_convert_finished(self, row, based_model_name, trained_model_name, plan_path,done):
        if row == -1:
            print("모델 신규 등록!!!!!!!!!!!!!!")
        if done:
            QMessageBox.information(None, "변환 작업 완료", f"{trained_model_name} 모델 변환 작업이 완료되었습니다\n영상 감지 및 기존 레이아웃을 불러옵니다.")
        else:
            QMessageBox.information(None, "변환 작업 완료", f"{trained_model_name} 모델 변환 작업이 완료되었습니다.")
        upload_thread = ModelUploadQThread(row, based_model_name, trained_model_name, plan_path)
        upload_thread.finished.connect(self.on_model_upload_finished)
        upload_thread.error.connect(self.on_model_upload_error)

        # 스레드 추적 (중복 방지)
        if not hasattr(self, "convert_threads"):
            self.upload_threads = {}
        self.upload_threads[based_model_name] = upload_thread

        upload_thread.start()

        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 취소 ]\n (상태: 학습 파일 업로드 중)")
        # model_description = view_model.index(row, 0).data()
        if self.convert_queue.empty():
            self.check_all_threads_finished()

    def on_path_convert_error(self, row, based_model_name, trained_model_name, msg):
        self.cleanup_upload_thread(based_model_name)
        QMessageBox.critical(self, "변환", f"[파일변환 실패] {trained_model_name} : {msg}")

        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 재학습 ]\n(상태: 오류)")
        view_model.dataChanged.emit(0, 5)
        
        model_description = view_model.index(row, 0).data()
        result = self.db_model_list.update(model_description=model_description, model_name=based_model_name,status=3)
        print(f'result: {result}')
        
    def on_path_convert_cancel(self, row):
        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 학습 ]")
        view_model.dataChanged.emit(0, 5)
        
    """
        트리톤 서버 내 모델 업로드 관련 함수
        on_model_upload_finished : 모델 업로드 Q스레드 시그널 이벤트 (finished)
        on_model_upload_error : 모델 업로드 Q스레드 시그널 이벤트 (error)

        cleanup_upload_thread: 모델 업로드 Q스레드 종료
    """
    def on_model_upload_finished(self, row, based_model_name, trained_model_name, plan_path):
        self.cleanup_upload_thread(based_model_name)
        time.sleep(2)  # 업로드 완료 후 잠시 대기
        # QMessageBox.information(self, "등록", f"[모델등록완료] {trained_model_name}:{plan_path}")

        view_model = self.tableview_model_list.model()
        if row != -1:
            view_model.setData(view_model.index(row, 4), "[ 학습 ]")
            view_model.dataChanged.emit(0, 5)

            model_description = view_model.index(row, 0).data()
            result = self.db_model_list.update(model_description=model_description, model_name=based_model_name, status=0)

            upload_dialog = AddTrainedModelDialog(self)
            if upload_dialog.exec():
                model_description = upload_dialog.line_edit_model_description.text()
                try:
                    date_str = "_".join(plan_path.split('_')[-2:])  # '20250424_180000'
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    date_obj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_data = self.db_model_list.insert(model_description=model_description, model_name=plan_path, model_registered_at=date_obj)
            
                if insert_data:
                    row = [model_description, "-", date_obj, "", "", ""]
                    QMessageBox.information(self, "성공", "AI 모델이 등록되었습니다")
                    
                    column_values = [model_description, self.dataset_config_file_path, f"{date_obj}", "", "[ 학습 ]", "[ 성능평가 ]"]
                    model = self.tableview_model_list.model()
                    row = model.rowCount() if model.rowCount() > 0 else 0

                    for col, text in enumerate(column_values):
                        item = QStandardItem(text)
                        item.setEditable(False)
                        item.setTextAlignment(Qt.AlignCenter)
                        model.setItem(row, col, item)
                    
                    self.dataset_config_file_path="-" # 데이터셋 경로 초기화
                    # TableView에 모델 연결
                    self.button_delegate_cell = CellButtonDelegate(self.img_path, parent=self.tableview_model_list)
                    self.tableview_model_list.setItemDelegate( self.button_delegate_cell)
                    self.button_delegate_cell.clicked.connect(self.handle_cell_clicked)
                else:
                    QMessageBox.critical(self, "실패", "AI 모델 등록 중 오류가 발생했습니다")
               
        else:
            model_description = based_model_name 

            try:
                date_str = "_".join(plan_path.split('_')[-2:])  # '20250424_180000'
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                date_obj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_data = self.db_model_list.insert(model_description=model_description, model_name=trained_model_name, model_registered_at=date_obj)
        
            if insert_data:
                row = [model_description, "-", date_obj, "", "", ""]
                QMessageBox.information(self, "성공", "AI 모델이 등록되었습니다")
                
                column_values = [model_description, "-", f"{date_obj}", "", "[ 학습 ]", "[ 성능평가 ]"]
                model = self.tableview_model_list.model()
                row = model.rowCount() if model.rowCount() > 0 else 0

                for col, text in enumerate(column_values):
                    item = QStandardItem(text)
                    item.setEditable(False)
                    item.setTextAlignment(Qt.AlignCenter)
                    model.setItem(row, col, item)
                
                self.dataset_config_file_path="-" # 데이터셋 경로 초기화
                # TableView에 모델 연결
                self.button_delegate_cell = CellButtonDelegate(self.img_path, parent=self.tableview_model_list)
                self.tableview_model_list.setItemDelegate( self.button_delegate_cell)
                self.button_delegate_cell.clicked.connect(self.handle_cell_clicked)
            else:
                QMessageBox.critical(self, "실패", "AI 모델 등록 중 오류가 발생했습니다")

        # self.sidebar.open_model_list_management_dialog()
    def on_model_upload_error(self, row, based_model_name, trained_model_name, msg):
        self.cleanup_upload_thread(based_model_name)
        QMessageBox.critical(self, "등록", f"[모델 등록 실패] {trained_model_name} : {msg}")

        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 4), "[ 재학습 ]\n(상태: 오류)")
        view_model.dataChanged.emit(0, 5)

        model_description = view_model.index(row, 0).data()
        result = self.db_model_list.update(model_description=model_description,model_name=based_model_name,status=3)
        print(f'result: {result}')

    def cleanup_upload_thread(self, model_name):
        thread = self.upload_threads.get(model_name)
        if thread:
            print(f"cleanup_upload_thread: {thread}")
            thread.quit()
            thread.wait()
            thread.deleteLater()
            del self.upload_threads[model_name]
            self.check_all_threads_finished() 


    """
        성능 평가 관련 함수
        handle_performance_evaluation_cell_clicked : 성능 평가 셀 클릭 이벤트
        
        on_performance_evaluation_started : 성능 평가 Q스레드 시그널 이벤트 (started)
        on_performance_evaluation_finished : 성능 평가 Q스레드 시그널 이벤트 (finished)
        on_performance_evaluation_error : 성능 평가 Q스레드 시그널 이벤트 (error)

        cleanup_performance_evaluation_thread : 성능 평가 Q스레드 종료
    """
    def handle_performance_evaluation_cell_clicked(self, row, model_name, dataset_config_file_path):
        print(f"row: {row}, model_name: {model_name}, dataset_config_file_path: {dataset_config_file_path}")
        performance_evaluation_thread = PerformanceEvaluationQThread(row, model_name, dataset_config_file_path)
        
        performance_evaluation_thread.started.connect(self.on_performance_evaluation_started)
        performance_evaluation_thread.finished.connect(self.on_performance_evaluation_finished)
        performance_evaluation_thread.error.connect(self.on_performance_evaluation_error)

        # 스레드 추적 (중복 방지)
        if not hasattr(self, "performance_evaluation_threads"):
            self.performance_evaluation_threads = {}

        self.performance_evaluation_threads[model_name] = performance_evaluation_thread
        performance_evaluation_thread.start()

    def on_performance_evaluation_started(self, row):
        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 5), "(상태: 성능 평가 진행 중)")

    def on_performance_evaluation_finished(self, row, model_name, value):
        self.cleanup_performance_evaluation_thread(model_name)
        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 5), "[ 성능평가 ]")
        model_description = view_model.index(row, 0).data()

        result = self.db_model_list.update(model_description=model_description, model_name=model_name, precision=value['precision'], recall=value['recall'], map50=value['map50'], map50_95=value['map50_95'], f1_score=value['f1_score'], speed=value['speed'])
        print(f'result: {result}')

    def on_performance_evaluation_error(self, row, model_name, msg):
        self.cleanup_performance_evaluation_thread(model_name)

        view_model = self.tableview_model_list.model()
        view_model.setData(view_model.index(row, 5), "[ 성능평가 ]")
        model_description = view_model.index(row, 0).data()

        QMessageBox.critical(self, "성능 평가", f"[성능 평가 실패] {model_description} : {msg}")

    def cleanup_performance_evaluation_thread(self, model_name):
        thread = self.performance_evaluation_threads.get(model_name)
        if thread:
            print(f"cleanup_performance_evaluation_thread: {thread}")
            thread.quit()
            thread.wait()
            thread.deleteLater()
            del self.performance_evaluation_threads[model_name]
            self.check_all_threads_finished() 

    # 모델 등록 버튼 클릭 이벤트
    def on_btn_add_new_model_clicked(self):
        add_new_model_dialog = AddNewModelDialog(self)

        if add_new_model_dialog.exec():
            model_description, model_name, model_file_path, dataset_config_file_path = add_new_model_dialog.get_add_model_info()
            self.dataset_config_file_path = dataset_config_file_path if dataset_config_file_path else '-'
            print(f"model_description: {model_description}, model_name: {model_name}, model_file_path: {model_file_path}, dataset_config_file_path: {dataset_config_file_path}")

            if model_file_path:
                print("PyTorch model file upload")
                # 폴더 생성
                source_pt_path = Path(model_file_path)
                if not source_pt_path.exists():
                    QMessageBox.critical(self, "오류", f"원본 .pt 파일이 존재하지 않습니다: {model_file_path}")
                    return
                experiment_base_dir = Path(os.getcwd()) / "experiments" # 현재 작업 디렉토리 기준
                print(f"experiment_base_dir: {experiment_base_dir}")
                target_experiment_path = experiment_base_dir / model_name / "weights"
                
                target_experiment_path.mkdir(parents=True, exist_ok=True)
                
                target_pt_path = target_experiment_path / "best.pt"

                shutil.copy2(source_pt_path, target_pt_path)
                print(f"'{source_pt_path}'를 '{target_pt_path}'로 복사했습니다.")

                # # 데이터셋 구성 파일 정보 저장 (선택 사항, 필요에 따라)
                # if dataset_config_file_path and dataset_config_file_path != '-':
                #     self.save_path_info(model_description, dataset_config_file_path)
                #     print(f"데이터셋 구성 파일 경로 저장: {model_description} -> {dataset_config_file_path}")
                    
                self.enqueue_convert_model(-1, model_description, model_name, Path(model_file_path))

    def on_btn_delete_model_clicked(self):
        selection_model = self.tableview_model_list.selectionModel()
        if not selection_model:
            QMessageBox.warning(self, "선택 오류", "삭제할 모델을 선택하세요.")
            return
        
        # selectedRows() 대신 selectedIndexes() 사용하여 셀 선택도 감지
        selected_indexes = selection_model.selectedIndexes()
        print(selected_indexes,"selected_indexes")
        
        # 선택된 셀이 없는 경우 체크
        if not selected_indexes:
            QMessageBox.warning(self, "선택 오류", "삭제할 모델을 선택하세요.")
            return
        
        # 선택된 셀의 행 정보 가져오기 (첫 번째 선택된 셀의 행 사용)
        view_model = self.tableview_model_list.model()
        row = selected_indexes[0].row()
        model_description = view_model.index(row, 0).data()
        
        if not model_description:
            QMessageBox.warning(self, "오류", "모델 정보를 가져올 수 없습니다.")
            return
        
        # 삭제 확인 대화상자
        result = QMessageBox.question(
            self, "삭제 확인", 
            f"'{model_description}' 모델을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            try:
                # 데이터베이스에서 삭제
                success = self.db_model_list.delete(model_description=model_description)
                
                if success:
                    # 테이블에서 행 제거
                    view_model.removeRow(row)
                    QMessageBox.information(self, "삭제 완료", f"'{model_description}' 모델이 삭제되었습니다.")
                else:
                    QMessageBox.warning(self, "삭제 실패", "모델 삭제에 실패했습니다.")
                    
            except Exception as e:
                QMessageBox.critical(self, "오류", f"모델 삭제 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        # 실행 중인 스레드가 있는지 확인
        self.threads_running = False
        
        # 모델 학습 스레드 확인
        if self.train_thread.is_work():
            self.threads_running = True
        
        # 모델 업로드 스레드 확인
        if self.upload_threads:
            self.threads_running = True
        
        # 성능 평가 스레드 확인
        if self.performance_evaluation_threads:
            self.threads_running = True
        
        # 파일 변환 작업 확인
        if self.converter_thread.is_work():
            self.threads_running = True
        
        if self.threads_running or self.train_stopped:
            # 실행 중인 스레드가 있는 경우
            self.hidden_pending_close = True
            print("실행 중인 스레드가 있습니다. 다이얼로그를 숨깁니다.")
            self.hide()
            event.ignore()
        else:
            # 실행 중인 스레드가 없는 경우
            self.train_stopped = False
            print("실행 중인 스레드가 없습니다. 다이얼로그를 종료합니다.")
            event.accept()
            
    def check_all_threads_finished(self):
        # 모든 스레드가 완료되었고 종료 대기 중인 경우
        if self.hidden_pending_close:
            print("현재 창이 invisible 상태입니다.")
            self.hidden_pending_close = False
            self.close()  # 다이얼로그 종료
    def showEvent(self, event):
        # 다이얼로그가 표시될 때 실행되는 코드
        print("다이얼로그가 표시되었습니다.")
        self.hidden_pending_close = False
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModelListManagementWidget(None,None)
    window.show()  
    sys.exit(app.exec())
