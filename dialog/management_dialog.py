import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from natsort import natsorted
from operator import attrgetter

from db.db_cctv_location import DbCctvLocation
from db.db_cctv_list import DbCctvList
from db.db_cctv_setting import DbCctvSetting
from ui.ui_management_dialog import Ui_Dialog

from widget.cctv_management_widget import CctvManagementWidget
from widget.event_logic_management_widget import EventLogicManagementWidget
from widget.model_management_widget import ModelListManagementWidget


class ManagementDialog(QWidget, Ui_Dialog):
    change_cctv_location = Signal()  # 카메라 위치 변경 시그널
    clicked_selected_location = Signal(list)  # 선택된 위치 클릭 시그널
    def __init__(self,temperary_layout=None,background_controller=None, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("관리")
        
        # 다이얼로그 인스턴스 추적을 위한 변수들
        self.clicked_location_arr=[]
        
        
        self.load_cctv_list_to_tree(self.tree_widget_management_side_bar)
        # 이전 선택 상태를 추적하기 위한 변수 추가(CCTV 필터링용)
        self.previously_selected_items = set()
        
        
        self.cctv_dialog = CctvManagementWidget()
        self.event_dialog = EventLogicManagementWidget()
        self.model_dialog = ModelListManagementWidget(temperary_layout,background_controller)
        self.dialog_stauts=None
        
        # 현재 표시 중인 콘텐츠 위젯 추적
        self.current_content_widget = self.label_management_widget
    
        # 트리 위젯 다중 선택모드 설정
        self.tree_widget_management_side_bar.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tree_widget_management_side_bar.itemSelectionChanged.connect(self.on_selection_changed)
        # 트리 위젯 클릭 이벤트 연결
        self.tree_widget_management_side_bar.itemClicked.connect(self.on_tree_item_clicked)
        
        self.tree_widget_management_side_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget_management_side_bar.customContextMenuRequested.connect(self.show_sidebar_context_menu)
        
    def on_tree_item_clicked(self, item, column):
        """트리 아이템 클릭 이벤트 처리"""
        item_text = item.text(column)
        # 순환 import 방지를 위해 각 함수 내부에서 import
         # CCTV, 이벤트, 모델 항목인지 확인
        is_menu_item = item_text in ["CCTV", "이벤트", "불안전 상황 감지", "모델 등록 및 학습"]
        
        if is_menu_item:            
            # 모든 선택 초기화
            self.tree_widget_management_side_bar.clearSelection()
            
            # 클릭한 메뉴 항목만 다시 선택
            item.setSelected(True)
            
            # 다중 선택 관련 변수 초기화
            self.clicked_location_arr = []
            self.previously_selected_items = set()
            
            # 시그널 차단 해제
            self.tree_widget_management_side_bar.blockSignals(False)
            
            # 내부 위젯에 빈 선택 목록 전달
            if hasattr(self, 'cctv_dialog') and self.cctv_dialog:
                self.cctv_dialog.filtered_cctv_list([])
        
        if item_text == "CCTV":
            self.open_cctv_management_dialog()
        elif item_text == "이벤트" or item_text == "불안전 상황 감지":
            self.open_event_logic_management_dialog()
        elif item_text =="모델 등록 및 학습":
            self.open_model_list_management_dialog()
            
    def on_selection_changed(self):
        """선택 상태가 변경될 때 호출되는 메서드"""
        # 현재 선택된 항목들 가져오기
        current_selected_items = self.tree_widget_management_side_bar.selectedItems()
        current_selected_locations = set()
        
        # 위치 항목들만 필터링 (CCTV의 하위 항목인 경우)
        for item in current_selected_items:
            if item.parent() and item.parent().text(0) == "CCTV":
                current_selected_locations.add(item.text(0))
        
        # 선택 항목
        selected = current_selected_locations - self.previously_selected_items
        
        # 선택 해제 항목
        unselected = self.previously_selected_items - current_selected_locations
        
        # 배열 업데이트
        for location in selected:
            if location not in self.clicked_location_arr:
                self.clicked_location_arr.append(location)
                print(f"위치 추가됨: {location}")
        
        for location in unselected:
            if location in self.clicked_location_arr:
                self.clicked_location_arr.remove(location)
                print(f"위치 제거됨: {location}")
        
        # 현재 상태 저장
        self.previously_selected_items = current_selected_locations
        
        # 변경된 배열 emit
        if self.clicked_location_arr:
            print(f"선택된 위치들: {self.clicked_location_arr}")
            self.cctv_dialog.filtered_cctv_list(self.clicked_location_arr)
        else:
            # 모든 선택이 해제된 경우
            # print("모든 위치 선택 해제됨")
            self.cctv_dialog.filtered_cctv_list([])
            
    def set_content_widget(self, new_widget):
        """
        콘텐츠 영역의 현재 위젯을 새 위젯으로 교체
        """
        if self.current_content_widget:
            # 기존 위젯 숨기기
            self.current_content_widget.hide()
            
            # 레이아웃에서 기존 위젯 제거
            self.layout_management.removeWidget(self.current_content_widget)
        
        # 새 위젯 설정
        self.layout_management.addWidget(new_widget)
        new_widget.show()

        # 현재 콘텐츠 위젯 업데이트
        self.current_content_widget = new_widget
        
        
    def open_cctv_management_dialog(self):
        """CCTV 관리 다이얼로그 열기"""
        try:
           # 새 위젯으로 교체
            self.set_content_widget(self.cctv_dialog)
            self.load_cctv_list_to_tree(self.tree_widget_management_side_bar, active_dialog='CCTV')
            self.dialog_stauts = 'CCTV'
        except Exception as e:
            print(f"CCTV 관리 다이얼로그 열기 오류: {e}")

    def open_event_logic_management_dialog(self):
        """이벤트 로직 관리 다이얼로그 열기"""
        try:
            self.set_content_widget(self.event_dialog)
            self.load_cctv_list_to_tree(self.tree_widget_management_side_bar, active_dialog='unsafe')
            self.dialog_stauts = 'event'
        except Exception as e:
            print(f"이벤트 로직 관리 다이얼로그 열기 오류: {e}")

    def open_model_list_management_dialog(self):
        """모델 목록 관리 다이얼로그 열기"""
        try:
            self.set_content_widget(self.model_dialog)
            self.load_cctv_list_to_tree(self.tree_widget_management_side_bar, active_dialog='unsafe')
            self.dialog_stauts = 'model'
        except Exception as e:
            print(f"모델 목록 관리 다이얼로그 열기 오류: {e}")
            
    def load_cctv_list_to_tree(self, tree_widget: QTreeWidget, active_dialog: str = None):

        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            top_item.setExpanded(True)  # 상위 항목 확장
            if top_item.text(0) == "관리":
                # 먼저 모든 메뉴 항목을 찾아둠 (나중에 접근하기 위해)
                cctv_menu_item = None
                event_menu_item = None
                
                # 메뉴 항목들을 미리 저장
                for j in range(top_item.childCount()):
                    menu_item = top_item.child(j)
                    menu_text = menu_item.text(0)
                    
                    if menu_text == "CCTV":
                        cctv_menu_item = menu_item
                    elif menu_text == "불안전 상황 감지":
                        event_menu_item = menu_item
                
                # 이제 각 항목을 처리
                for j in range(top_item.childCount()):
                    child_item = top_item.child(j)
                    child_text = child_item.text(0)
                    
                    if child_text == "CCTV":
                        self.clear_cctv_children(child_item)  # 기존 CCTV 하위 항목 제거
                        
                        cctv_location = DbCctvLocation()
                        rows = cctv_location.select()
                        
                        # camera_location 속성을 기준으로 자연 정렬
                        rows = natsorted(rows, key=attrgetter('camera_location'))
                        
                        location_items = {}
                        for row in rows:
                            location = row.camera_location
                            if location not in location_items:
                                location_item = QTreeWidgetItem([location])
                                child_item.addChild(location_item)
                                location_items[location] = location_item
                            else:
                                location_item = location_items[location]
                        
                        # CCTV가 활성화되면 CCTV를 펼치고 다른 메뉴는 접음
                        if active_dialog == 'CCTV':
                            child_item.setExpanded(True)
                            # 불안전 상황 감지 메뉴 접기
                            if event_menu_item:
                                event_menu_item.setExpanded(False)
                    

                    elif child_text == "불안전 상황 감지":
                        # 불안전 상황이 활성화되면 불안전 상황을 펼치고 다른 메뉴는 접음
                        if active_dialog == 'unsafe':
                            child_item.setExpanded(True)
                            # CCTV 메뉴 접기
                            if cctv_menu_item:
                                cctv_menu_item.setExpanded(False)
                        else:
                            # active_dialog가 CCTV인 경우 불안전 상황 감지 접기
                            if active_dialog == 'CCTV':
                                child_item.setExpanded(False)
                
    def clear_cctv_children(self, cctv_item):
        """CCTV 항목의 모든 하위 항목 제거"""
        try:
            # 하위 항목이 있는지 확인
            child_count = cctv_item.childCount()
            if child_count > 0:
                
                # 모든 하위 항목 제거 (역순으로 제거하는 것이 안전)
                for i in range(child_count - 1, -1, -1):
                    child = cctv_item.child(i)
                    cctv_item.removeChild(child)

        except Exception as e:
            print(f"CCTV 하위 항목 제거 중 오류 발생: {e}")
            
    def show_sidebar_context_menu(self, position):
        #트리 위젯의 우클릭(컨텍스트) 메뉴를 표시#
        item = self.tree_widget_management_side_bar.itemAt(position)
        
        if (item):
            # "위치" 항목인 경우 (추가 메뉴만 표시)
            if item.text(0) == "CCTV":
                menu = QMenu()
                add_action = menu.addAction("공장 추가")
                
                action = menu.exec_(self.tree_widget_management_side_bar.viewport().mapToGlobal(position))
                if action == add_action:
                    print("위치 추가 클릭됨")
                    self.on_add_location_clicked()
                    
            # 위치의 하위 항목인 경우 (수정, 삭제 메뉴 표시)
            elif item.parent() and item.parent().text(0) == "CCTV":
                menu = QMenu()
                edit_action = menu.addAction("수정")
                delete_action = menu.addAction("삭제")
                
                action = menu.exec_(self.tree_widget_management_side_bar.viewport().mapToGlobal(position))
                if action == edit_action:
                    print(f"위치 수정 클릭됨: {item.text(0)}")
                    self.edit_location(item.text(0))
                elif action == delete_action:
                    print(f"위치 삭제 클릭됨: {item.text(0)}")
                    self.delete_location(item.text(0))

    def on_add_location_clicked(self):
        # 카메라 위치 추가
        text, ok = QInputDialog.getText(
            self, 
            '위치 추가', 
            '추가하고자 하는 공장명을 입력하십시오:', 
            QLineEdit.Normal
        )

        if ok and text:  # 사용자가 OK를 클릭하고 텍스트가 비어있지 않은 경우
            # 새로운 위치 정보를 CameraLocation DB에 추가
            camera_location = DbCctvLocation()
            camera_location.camera_location = text
            camera_location.insert()

            self.load_cctv_list_to_tree(self.tree_widget_management_side_bar)
            QMessageBox.information(self, '성공', '새로운 위치가 추가되었습니다.') 
        
    def edit_location(self, location_name):
        #카메라 위치 정보 수정
        text, ok = QInputDialog.getText(
            self, 
            '위치 수정', 
            '수정할 공장명을 입력하십시오:', 
            QLineEdit.Normal,
            location_name
        )
        
        if ok and text and text != location_name:  # 변경된 값이 있는 경우에만 처리
            # 저장된 순서 불러오기
            
            # DB 위치 정보 업데이트
            camera_location = DbCctvLocation()
            camera_location.camera_location=text
            camera_location.update(camera_location=location_name)
            
            # CameraList의 item.camera_location 값도 업데이트
            camera_list = DbCctvList()
            camera_list.camera_location= text
            camera_list.update(camera_location=location_name)
            
            camera_setting = DbCctvSetting()
            camera_setting.camera_location = text
            camera_setting.update(camera_location=location_name)
            
            self.load_cctv_list_to_tree(self.tree_widget_management_side_bar)
            QMessageBox.information(self, '성공', '위치가 수정되었습니다.')
            self.change_cctv_location.emit()
            
    def delete_location(self, location_name):

        # 해당 위치에 카메라가 있는지 확인
        camera_list = DbCctvList().select(camera_location=location_name)
        if camera_list:
            QMessageBox.warning(self, '삭제 불가', 
                            '이 위치에 등록된 카메라가 있습니다.\n먼저 카메라를 삭제해주세요.')
            return
        
        reply = QMessageBox.question(self, '삭제 확인',
                                f'{location_name}을(를) 삭제하시겠습니까?',
                                QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 저장된 순서 불러오기
            
            # DB에서 위치 삭제
            camera_location = DbCctvLocation()
            camera_location.delete(location_name)
            
            # UI 업데이트
            self.load_cctv_list_to_tree(self.tree_widget_management_side_bar)
            QMessageBox.information(self, '성공', '위치가 삭제되었습니다.')  
            self.change_cctv_location.emit() 
    def closeEvent(self, event):
        # print("현재 위치",self.dialog_stauts)
        if self.dialog_stauts=='model':
            self.model_dialog.close()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ManagementDialog()
    widget.show()  
    sys.exit(app.exec())