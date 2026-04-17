# cctv_setting_dialog.py
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ast
from PySide6.QtWidgets import *
from PySide6 import QtGui, QtCore
from PySide6.QtCore import *
from PySide6.QtGui import *

from ui.ui_cctv_setting_dialog import Ui_Dialog
from widget.ai_event_log_search_cctv_list_widget import AiEventLogSearchCctvListWidget
from db.db_cctv_list import DbCctvList
from db.db_cctv_setting import DbCctvSetting

from db.db_logic_list import DbLogicList
from dialog.cctv_setting_event_dialog import CctvSettingEventDialog  # 추가: 이벤트 설정 위젯 import
from setting.use_qsetting import Setting  # 추가: UseQSetting 모듈 import
class ReadOnlyDelegate(QStyledItemDelegate):
    """읽기 전용 델리게이트 - 편집을 막음"""
    def createEditor(self, parent, option, index):
        # 편집기를 생성하지 않음으로써 편집을 방지
        return None
    
class CctvSettingDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("설정")
        
        # 테이블 업데이트 중인지 확인하기 위한 플래그 추가
        self.is_loading_table = False

        self.script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리
        self.script_dir = os.path.dirname(self.script_dir)  # 한 단계 상위 폴더

        self.init_ui()
        self.calculate_and_update_rps()  # RPS 계산 및 업데이트

    def init_ui(self):
        #UI 초기화 및 이벤트 연결

        readonly_delegate = ReadOnlyDelegate()
        self.tablewidget_cctv_setting.setItemDelegateForColumn(0, readonly_delegate)
        
        self.tablewidget_cctv_setting.cellDoubleClicked.connect(self.open_setting_event_dialog) # tablewidget_cctv_setting 더블클릭 이벤트 연결 - 이벤트 설정 창 송출
        # self.tablewidget_cctv_setting.cellChanged.connect(self.update_fps_limit_in_db)  # fps 설정 값 변경 이벤트 연결
       
        sidebar = AiEventLogSearchCctvListWidget() # 카메라 목록 위젯 적용
        self.SideBar.replaceWidget(self.label_cctv_list_widget, sidebar)
        self.label_cctv_list_widget.deleteLater()
        
        sidebar.selected_cctv_changed.connect(self.filter_camera_list)  # 선택된 카메라 변경 시 필터링
        self.load_cctv_list()

    @Slot()
    def filter_camera_list(self, selected_items):
        """선택된 CCTV만 테이블에 표시"""
        print(f"선택된 CCTV: {selected_items}")
        
        # 필터링 조건이 없으면 모든 행 표시
        if not selected_items:
            for row in range(self.tablewidget_cctv_setting.rowCount()):
                self.tablewidget_cctv_setting.setRowHidden(row, False)
            return
        
        # 선택된 카메라에 해당하는 위치 목록 (헤더 행 표시용)
        camera_locations = set()
        
        # 먼저 각 카메라가 어떤 위치에 속하는지 확인
        for row in range(self.tablewidget_cctv_setting.rowCount()):
            camera_name_item = self.tablewidget_cctv_setting.item(row, 0)
            if not camera_name_item:
                continue
            
            camera_name = camera_name_item.text()
            
            # 카메라 행인지 확인 (헤더 행이 아닌 경우)
            if camera_name_item.background().color().name() != "#fff0be":
                # 선택된 카메라 목록에 있는 경우
                if camera_name in selected_items:
                    # 상위 위치 찾기
                    for prev_row in range(row-1, -1, -1):
                        prev_item = self.tablewidget_cctv_setting.item(prev_row, 0)
                        if prev_item and prev_item.background().color().name() == "#fff0be":
                            camera_locations.add(prev_item.text())
                            break
        
        # 각 행을 순회하며 필터링 적용
        for row in range(self.tablewidget_cctv_setting.rowCount()):
            camera_name_item = self.tablewidget_cctv_setting.item(row, 0)
            if not camera_name_item:
                continue
            
            camera_name = camera_name_item.text()
            
            # 헤더 행인지 확인
            is_header = camera_name_item.background().color().name() == "#fff0be"
            
            if is_header:
                # 위치 헤더 행인 경우 - 해당 위치에 선택된 카메라가 있으면 표시
                location_name = camera_name
                self.tablewidget_cctv_setting.setRowHidden(row, location_name not in camera_locations)
            else:
                # 카메라 행인 경우 - 선택된 카메라면 표시, 아니면 숨김
                self.tablewidget_cctv_setting.setRowHidden(row, camera_name not in selected_items)

    def _get_location_order(self):
        """Retrieve location order from settings."""
        settings = Setting()
        saved_order = settings.get("sidebar_order")
        location_order_dict = {}

        if saved_order:
            try:
                order_data = ast.literal_eval(saved_order)
                for management_name, management_data in order_data.items():
                    for item_data in management_data:
                        for subitem_data in item_data["children"]:
                            if subitem_data["name"] == "카메라 목록" and "children" in subitem_data:
                                for idx, loc_data in enumerate(subitem_data["children"]):
                                    location_order_dict[loc_data["name"]] = idx
            except (ValueError, SyntaxError):
                pass  # Handle invalid saved_order gracefully

        return location_order_dict

    """QSettings 값 기준으로 Sidebar /tablewidget_cctv_setting 내용 정렬 """

    def load_cctv_list(self):
        # SideBar 정렬
        # Qsettings 기준 정렬 오류, 추후 수정 필요
        self.is_loading_table = True  # Set loading flag

        # Clear table
        self.tablewidget_cctv_setting.setRowCount(0)

        # Get camera data and location order
        camera_list = DbCctvSetting().select()
        location_order_dict = self._get_location_order()
        # Group cameras by location
        grouped_data_dict = self._group_cameras_by_location(camera_list)

        # Sort locations
        sorted_locations = sorted(
            grouped_data_dict.keys(),
            key=lambda loc: self._sort_key_location(loc, location_order_dict)
        )

        # Populate table
        row_idx = 0
        for location in sorted_locations:
            # Add location header row
            self.tablewidget_cctv_setting.insertRow(row_idx)
            location_item = QTableWidgetItem(location)
            location_item.setBackground(QColor(255, 240, 190))
            location_item.setTextAlignment(Qt.AlignCenter)
            self.tablewidget_cctv_setting.setItem(row_idx, 0, location_item)
            for col in range(1, 2):
                empty_item = QTableWidgetItem("-")
                empty_item.setBackground(QColor(255, 240, 190))
                empty_item.setTextAlignment(Qt.AlignCenter)
                self.tablewidget_cctv_setting.setItem(row_idx, col, empty_item)
            row_idx += 1

            # Add sorted cameras for this location
            sorted_cameras = sorted(
                grouped_data_dict[location],
                key=self._sort_key_camera_name
            )
            for camera in sorted_cameras:
                self.tablewidget_cctv_setting.insertRow(row_idx)
                name_item = QTableWidgetItem(camera.camera_name)
                # fps_item = QTableWidgetItem(str(camera.fps_limit) if camera.fps_limit is not None else "-")
                event_item = QTableWidgetItem(camera.unsafe_event if camera.unsafe_event is not None else "-")

                # Center-align text
                for item in [name_item, event_item]:
                    item.setTextAlignment(Qt.AlignCenter)

                # Set table items
                self.tablewidget_cctv_setting.setItem(row_idx, 0, name_item)
                # self.tablewidget_cctv_setting.setItem(row_idx, 1, fps_item)
                self.tablewidget_cctv_setting.setItem(row_idx, 1, event_item)
                row_idx += 1
        header = self.tablewidget_cctv_setting.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch) # 열 너비를 현재 창 크기에 맞게 균등 조정   
        self.is_loading_table = False  # Clear loading flag


    
    def _sort_key_location(self, location, location_order_dict):
        """Define sort key for camera_location."""
        if location in location_order_dict:
            return location_order_dict[location]
        try:
            return int(''.join(filter(str.isdigit, location)))
        except ValueError:
            return float('inf')  # Sort non-numeric locations to the end

    def _sort_key_camera_name(self, setting):
        """Define sort key for camera_name."""
        try:
            return int(''.join(filter(str.isdigit, setting.camera_name)))
        except ValueError:
            return float('inf')  # Sort non-numeric names to the end

    def _group_cameras_by_location(self, camera_list):
        """Group camera settings by camera_location."""
        grouped_data_dict = {}
        for camera in camera_list:
            if camera.camera_location not in grouped_data_dict:
                grouped_data_dict[camera.camera_location] = []
            grouped_data_dict[camera.camera_location].append(camera)
        return grouped_data_dict
    
    

    def open_setting_event_dialog(self, row, column):
        # cctv 이벤트 설정 다이얼 로그 열기
        if column == 1:  # 2번째 열(위험 이벤트 설정)만 처리
            camera_name_item = self.tablewidget_cctv_setting.item(row, 0)  # 1번째 열의 camera_name
            
            if camera_name_item:
                camera_name = camera_name_item.text()
                
                # 헤더 행인지 확인 (배경색으로 판별)
                if camera_name_item.background().color().name() == "#fff0be":
                    return  # 헤더 행이면 처리하지 않음
                
                # 이벤트 설정 위젯 생성 및 표시
                self.event_setting_widget = CctvSettingEventDialog(camera_name, self)
                self.event_setting_widget.event_updated.connect(self.on_event_updated)
                self.event_setting_widget.show()
        
    def calculate_and_update_rps(self):
        """현재 CCTV 설정의 unsafe_event를 기반으로 RPS 계산 및 업데이트"""
        try:
            # 모든 CCTV 설정 가져오기
            camera_settings = DbCctvSetting().select()
            
            total_rps = 0.0
            db_logic = DbLogicList()
            
            for camera in camera_settings:
                if camera.unsafe_event:
                    # unsafe_event는 쉼표로 구분된 이벤트 이름들
                    event_names = [event.strip() for event in camera.unsafe_event.split(',') if event.strip()]
                    
                    for event_name in event_names:
                        # 각 이벤트의 skip_frame 값 조회
                        logic_results = db_logic.select(logic_name=event_name)
                        
                        if logic_results:
                            skip_frame = logic_results[0].skip_frame
                            if skip_frame < 1:
                                skip_frame = 1
                            # 30/(skip_frame+1) 공식으로 RPS 계산
                            rps_value = 30.0 / skip_frame
                            total_rps += rps_value
                            print(f"Camera: {camera.camera_name}, Event: {event_name}, Skip Frame: {skip_frame}, RPS: {rps_value:.2f}")
            
            # 계산된 총 RPS 값을 label에 설정
            self.label_use_rps_value.setText(f"{int(total_rps)}")
            self.label_free_rps_value.setText(f"{int(600 - total_rps)}")
            print(f"Total RPS: {total_rps:.1f}")
            
        except Exception as e:
            print(f"RPS 계산 중 오류 발생: {e}")
            self.label_use_rps_value.setText("0.0")
    
    def on_event_updated(self, camera_name, events):
        # 변경 이벤트 설정 DB에 업데이트
        print("이벤트 업데이트:", camera_name, events)
        cctv = DbCctvSetting()
        cctv.camera_name = camera_name
        cctv.unsafe_event = events  # events가 None이면 DB에 null로 저장됨
        cctv.update(camera_name=camera_name)
        
        self.db_cctv_list = DbCctvList()
        self.db_cctv_list.camera_name = camera_name
        self.db_cctv_list.unsafe_event = events  # 카메라의 이벤트 설정 업데이트
        self.db_cctv_list.update(camera_name=camera_name)  # 카메라 정보 업데이트
        # 테이블 업데이트
        self.load_cctv_list()
        # RPS 재계산 및 업데이트
        self.calculate_and_update_rps()

    def on_cctv_item_clicked(self, item, column):
        #cctvList 항목 클릭 시 호출
        if item.childCount() > 0:  # camera_location 항목인 경우
            is_selected = item.isSelected()
            for i in range(item.childCount()):
                child = item.child(i)
                child.setSelected(is_selected)  # 부모 항목의 선택 상태와 동일하게 설정

    def update_fps_limit_in_db(self, row, column):
        # 2번째 열(fps_limit) 변경 시 DB 업데이트 

        # 테이블 로딩 중일 때는 함수 실행하지 않음
        if self.is_loading_table:
            return
            
        if column == 1:  # 2번째 열(fps_limit)만 처리
            camera_name_item = self.tablewidget_cctv_setting.item(row, 0)  # 1번째 열의 camera_name
            fps_limit_item = self.tablewidget_cctv_setting.item(row, column)  # 2번째 열의 fps_limit

            if camera_name_item and fps_limit_item:
                camera_name = camera_name_item.text()
                try:
                    # "-" 값이나 빈 값은 무시
                    if fps_limit_item.text() == "-" or not fps_limit_item.text().strip():
                        return
                    fps_limit = int(fps_limit_item.text())  # fps_limit 값을 정수로 변환
                except ValueError:
                    QMessageBox.warning(self, "입력 오류", "fps_limit 값은 정수여야 합니다.")
                    # print("fps_limit 값은 정수여야 합니다.", fps_limit_item.text())
                    self.load_cctv_list()  # 잘못된 입력 시 테이블을 다시 로드
                    return

                # DB 업데이트
                cctv = DbCctvSetting()
                cctv.camera_name = camera_name
                cctv.fps_limit = fps_limit
                cctv.update(camera_name=camera_name)

                QMessageBox.information(self, "성공", f"{camera_name}의 fps_limit 값이 {fps_limit}으로 업데이트되었습니다.")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CctvSettingDialog()
    window.show()  
    sys.exit(app.exec()) 

   




