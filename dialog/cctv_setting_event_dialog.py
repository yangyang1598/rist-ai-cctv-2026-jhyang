# cctv_setting_event_dialog.py
from PySide6.QtWidgets import QDialog, QMessageBox, QListWidgetItem, QVBoxLayout
from PySide6.QtCore import Signal, QTimer, Qt
from ui.ui_cctv_event_setting import Ui_Dialog
from db.db_cctv_setting import DbCctvSetting
from dialog.cctv_setting_event_select_dialog import CctvSettingEventSelectDialog  # SelectEvent 클래스 임포트 추가
from widget.ai_event_log_search_event_list_widget import AiEventLogSearchEventListWidget


class CctvSettingEventDialog(QDialog, Ui_Dialog):
    # 이벤트 업데이트 시그널 정의 (카메라 이름과 설정된 이벤트 목록 전달)
    event_updated = Signal(str, str)
    
    def __init__(self, camera_name, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(f"이벤트 설정 - {camera_name}")
        
        self.current_events_arr = []
        self.camera_name = camera_name
        # 카메라 이름 설정
        self.label_cctvname.setText(camera_name)
        
        # event_list_widget에 AiEventLogSearchEventListWidget 추가
        self.event_search_widget = AiEventLogSearchEventListWidget()
        self.event_list_widget.setLayout(QVBoxLayout())
        self.event_list_widget.layout().addWidget(self.event_search_widget)
        
        self.load_current_events()# 현재 카메라에 설정된 이벤트 불러오기
        self.update_event_lists()# 이벤트 목록 업데이트
        
        # 버튼 이벤트 연결
        self.button_add_event.clicked.connect(self.on_add_event)
        self.button_cancel_event.clicked.connect(self.on_cancel_event)
        self.button_ok.clicked.connect(self.on_ok_button_clicked)
        
        
    

    
    def load_current_events(self):
        # 카메라에 설정된 이벤트 불러오기
        try:
            settings = DbCctvSetting().select(camera_name=self.camera_name)[0]
            if settings and settings.unsafe_event:
                self.current_events_arr = [event.strip() for event in settings.unsafe_event.split(',')]
            else:
                self.current_events_arr = []
        except Exception as e:
            print(f"이벤트 로드 중 오류 발생: {e}")
            self.current_events_arr = []
    
    def update_event_lists(self):
        # 전체 이벤트 목록 및 현재 설정된 이벤트 목록 업데이트

        # SetEventList 초기화
        self.listwidget_set_event_list.clear()
        
        # 새로운 이벤트 검색 위젯에서 현재 설정된 이벤트들을 체크 상태로 설정
        for row in range(self.event_search_widget.model.rowCount()):
            item = self.event_search_widget.model.item(row)
            event_name = item.text()
            if event_name in self.current_events_arr:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
        
        # SetEventList에도 체크박스 형식으로 현재 설정된 이벤트 추가 (체크 해제 상태로)
        for event in self.current_events_arr:
            item = QListWidgetItem(self.listwidget_set_event_list)
            checkbox_widget = CctvSettingEventSelectDialog(event)
            checkbox_widget.checkbox.setChecked(False)  # 기본적으로 체크 해제 상태로 추가
            item.setSizeHint(checkbox_widget.sizeHint())
            self.listwidget_set_event_list.setItemWidget(item, checkbox_widget)
    """ 이벤트 추가 /제거 /설정 """
    def on_add_event(self):
        # 이벤트 추가 버튼 클릭 시 호출
        checked_events_arr = []
        
        # 새로운 이벤트 검색 위젯에서 체크된 이벤트들 가져오기
        selected_events = self.event_search_widget.get_selected_items_dict()
        
        for event in selected_events:
            if event not in self.current_events_arr:
                checked_events_arr.append(event)
        
        if not checked_events_arr:
            QMessageBox.information(self, "알림", "추가할 이벤트를 선택해주세요.")
            return
        
        # 현재 이벤트 목록에 추가
        self.current_events_arr.extend(checked_events_arr)
        
        # 이벤트 목록 업데이트
        self.update_event_lists()
    
    def on_cancel_event(self):
        # 이벤트 취소(제거) 버튼 클릭 시 호출
        events_to_remove = []
        
        for i in range(self.listwidget_set_event_list.count()):
            item = self.listwidget_set_event_list.item(i)
            checkbox_widget = self.listwidget_set_event_list.itemWidget(item)
            if checkbox_widget.checkbox.isChecked():  # 체크된 항목을 찾음 (삭제 대상)
                events_to_remove.append(checkbox_widget.checkbox.text())
        
        if not events_to_remove:
            QMessageBox.information(self, "알림", "제거할 이벤트를 체크해주세요.")
            return
        
        # 확인 메시지 표시
        if len(events_to_remove) > 0:
            confirm_msg = f"체크한 {len(events_to_remove)}개의 이벤트를 제거하시겠습니까?"
            reply = QMessageBox.question(self, "이벤트 제거 확인", confirm_msg,
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # 선택된 이벤트를 현재 이벤트 목록에서 제거
                for event_name in events_to_remove:
                    if event_name in self.current_events_arr:
                        self.current_events_arr.remove(event_name)
                
                # 이벤트 목록 업데이트
                self.update_event_lists()
                # QMessageBox.information(self, "알림", f"{len(events_to_remove)}개의 이벤트가 제거되었습니다.")
    
    def on_ok_button_clicked(self):
        # 설정 버튼 클릭 시 호출

        # 현재 SetEventList에 있는 체크 해제된 항목만 저장 (체크된 항목은 삭제할 대상이므로 제외)
        self.current_events_arr = []
        for i in range(self.listwidget_set_event_list.count()):
            item = self.listwidget_set_event_list.item(i)
            checkbox_widget = self.listwidget_set_event_list.itemWidget(item)
            if not checkbox_widget.checkbox.isChecked():  # 체크 해제된 항목만 저장
                self.current_events_arr.append(checkbox_widget.checkbox.text())
                
        # DB에 저장 및 변경 알림
        self.save_events()
        
        QMessageBox.information(self, "카메라 데이터 변경", "변경된 설정 값은 프로그램 재실행 시 적용됩니다.")
        # 창 닫기
        self.close()
    
    def save_events(self):
        # 현재 설정된 이벤트를 DB에 저장

        print("저장된 이벤트:", self.current_events_arr)
        if not self.current_events_arr:
            # 이벤트 목록이 비어있으면 None을 전달하여 DB에서 null로 저장되도록 함
            print("이벤트가 비어있음")
            self.event_updated.emit(self.camera_name, None)
        else:
            events_str = ', '.join(self.current_events_arr)
            # 이벤트 업데이트 시그널 발생
            self.event_updated.emit(self.camera_name, events_str)
