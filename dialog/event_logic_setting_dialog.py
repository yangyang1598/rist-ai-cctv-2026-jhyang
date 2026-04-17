from ultralytics import YOLO  # YOLO 모델 클래스 임포트
from PySide6.QtWidgets import QWidget, QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal,QTimer

from setting import paths
from setting.use_qsetting import Setting
from ui.ui_event_logic_setting import Ui_Dialog
from db.db_model_list import DbModelList  # ModelList 클래스 임포트
from event_logic.setup_event_logic import SetupEventLogic  # SetupEventLogic 클래스 임포트

class EventLogicSettingDialog(QDialog, Ui_Dialog):
    """
    이벤트 로직 설정 다이얼로그 클래스
    ui_EventLogicSetting.py를 기반으로 한 이벤트 로직 설정 기능을 제공합니다.
    """
    # 선택된 로직 정보를 전달하기 위한 시그널 정의
    signal_logic_selected = Signal(dict)
    signal_error_Qmessagebox = Signal(str,str)  # 오류 발생 시그널 정의
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("이벤트 로직 설정")
        
        self.setWindowModality(Qt.WindowModal)# 모달 대화상자로 설정
        self.setFixedSize(self.size())# 대화상자 크기 조정 방지
        
        # 초기 상태 설정
        self.radio_ai.setChecked(True) # 기본적으로 AI 모델 선택
        self.frame.setVisible(True) # AI 모델 프레임 표시
        self.frame_2.setVisible(False) # 알고리즘 프레임 숨김
        
        self.model_class_info = {}  # 모델 클래스 정보 초기화
        
        self.radio_ai.clicked.connect(self.selected_toggle)
        self.radio_algorithm.clicked.connect(self.selected_toggle)
        self.button_accept.clicked.connect(self.clicked_accept_event)
        self.combo_ai.currentIndexChanged.connect(self.selected_combo_ai)  # 모델 선택 이벤트 연결

        self.load_options() # 모델 및 알고리즘 옵션 로딩
        
    def selected_toggle(self):
        # 라디오 버튼에 따라 프레임 표시 전환
        
        if self.radio_ai.isChecked():
            self.frame.setVisible(True)
            self.frame_2.setVisible(False)
        else:
            self.frame.setVisible(False)
            self.frame_2.setVisible(True)
               
    def load_options(self):
        # AI 모델 콤보박스에 ModelList에서 모델 목록 가져와 추가
        try:
            # 기존 항목 초기화
            self.combo_ai.clear()
            
            # ModelList에서 모든 모델 목록 가져오기
            model_list = DbModelList().select()

            # 모델이 하나도 없는 경우 기본값 추가
            if not model_list:
                self.combo_ai.addItem("YOLO v8 (물체 검출)")
                self.combo_ai.addItem("불티 비산/훈소 감지")
            else:
                # DB에서 가져온 모델 목록 추가
                model_list.sort(key=lambda model:model.model_description)
                for model in model_list:
                    display_text = f"{model.model_description}"
                    self.combo_ai.addItem(display_text, model.model_name)  # 두 번째 인자로 모델 ID를 추가하여 나중에 참조 가능
        except Exception as e:
            # 오류 발생 시 사용자에게 알림
            QMessageBox.warning(self, "데이터베이스 오류", f"모델 목록을 불러오는 중 오류가 발생했습니다: {str(e)}")
            
           
        # 객체 콤보박스에 옵션 추가
        self.combo_object.clear()
        # print(self.model_class_info," 모델 클래스 정보 초기화")
        if self.combo_ai.count() > 0: # 콤보박스에 아이템이 있을 때만 실행
             QTimer.singleShot(0, self.selected_combo_ai)
        
        # 알고리즘 콤보박스에 옵션 추가, Hardcoding 
        self.combo_algorithm.clear()

        setting_keys: dict =  Setting(paths.GLOBAL_SETTING_PATH).to_dict()
        logic_keys = setting_keys.get("logic_list", {})
        for key in logic_keys:
            self.combo_algorithm.addItem(key)

    def selected_combo_ai(self):
        # 선택된 모델의 가용 label 정보 가져와 combo_object에 추가
        try:
            # 현재 선택된 인덱스가 유효한지 확인
            current_idx = self.combo_ai.currentIndex()
            if current_idx < 0:
                return

            # 선택된 모델 ID 가져오기
            model_name= self.combo_ai.currentData()
            # 모델 ID를 사용하여 DB에서 모델 정보 가져오기
            models = DbModelList().select(model_name=model_name)
            if not models:
                return
                
            model = models[0]
            
            # YOLO 모델 경로 구성 (grpc 서버 URL)
            model_path = f"grpc://[::1]:8001/{model.model_name}"
            
            # YOLO 모델 로드
            try:
                yolo = YOLO(model_path, task="detect")
                
                # 객체 목록 업데이트
                self.combo_object.clear()
                self.model_class_info.clear()
                
                # YOLO 모델이 감지할 수 있는 객체 이름 가져오기
                if hasattr(yolo, 'names') and yolo.names:
                    for idx, name in yolo.names.items():
                        self.combo_object.addItem(name)
                        self.model_class_info[name] = idx
                # else:
                #     # 이름 정보가 없으면 기본값 설정
                #     self.combo_object.addItem("사람")
                #     self.combo_object.addItem("차량")
                    
            except Exception as e:
                print(f"YOLO 모델 로드 오류: {str(e)}")
                # 오류 발생 시 기본 객체 목록 사용
                self.combo_object.clear()
                self.model_class_info.clear()
                error_title = "모델 객체 값 오류"
                error_message = f"트라이톤 서버 내 해당 모델이 존재하지 않거나 로드 중 오류가 발생했습니다: {str(e)}"
                if 'NOT_FOUND' in str(e): 
                    error_message = "트라이톤 서버 내 해당 모델이 존재하지않습니다."
               
                self.signal_error_Qmessagebox.emit(error_title, error_message) # 시그널 발생
                
        except Exception as e:
            print(f"모델 선택 처리 오류: {str(e)}")
            error_title = "모델 선택 오류"
            error_message = f"선택한 모델을 처리하는 중 오류가 발생했습니다: {str(e)}"
           
            self.signal_error_Qmessagebox.emit(error_title, error_message) # 시그널 발생
        
    def clicked_accept_event(self):
        #선택된 로직 정보를 부모 위젯에 전달하고 대화상자를 닫음
        
        logic_info_dict = self.get_custom_logic_order()

        # 시그널 발생
        print(f"선택된 로직 정보: {logic_info_dict}")
        self.signal_logic_selected.emit(logic_info_dict)
        
        # 대화상자 닫기
        self.accept()

    def get_custom_logic_order(self):
        # 지정한 로직 정보를 딕셔너리 형태로 반환
        
        logic_info_dict = {}
        
        if self.radio_ai.isChecked():
            logic_info_dict["type"] = "AI"
            logic_info_dict["name"] = self.combo_ai.currentText()
            logic_info_dict["model"] = self.combo_ai.currentData()  # 선택된 모델의 ID 값도 함께 저장
            logic_info_dict["object"] = self.combo_object.currentText()
            logic_info_dict["object_index"] = self.model_class_info[self.combo_object.currentText()]
        else:
            logic_info_dict["type"] = "algorithm"
            logic_info_dict["name"] = self.combo_algorithm.currentText()
            logic_info_dict["model"] = None
            logic_info_dict["object"] = None
            logic_info_dict["object_index"] = None
            
        return logic_info_dict
        