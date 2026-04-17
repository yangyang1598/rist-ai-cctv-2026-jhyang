import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication, QTableWidgetItem, QDialog, QHeaderView
from PySide6.QtCore import Slot

from db.db_logic_list import DbLogicList
from db.db_cctv_list import DbCctvList
from db.db_cctv_setting import DbCctvSetting
from ui.ui_event_logic_management_widget import Ui_Widget
from dialog.event_logic_add_dialog import EventLogicAddDialog
class EventLogicManagementWidget(QDialog, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)     
        
        self.get_db_logic_list = DbLogicList()
        self.cctv_list=DbCctvList()
        self.cctv_setting=DbCctvSetting()
        self.button_add_event.clicked.connect(self.add_event_clicked)
        self.button_delete_event.clicked.connect(self.delete_event_clicked)
        self.tablewidget_event_list.cellDoubleClicked.connect(self.edit_event_content)  # 테이블 셀 더블 클릭 시 이벤트 추가
        
        self.init_ui()
             
    def init_ui(self):
        
        event_list= self.get_db_logic_list.select()
        # logic_name 기준으로 오름차순 정렬
        event_list.sort(key=lambda item: item.logic_name)
        
        self.tablewidget_event_list.setRowCount(0) # 테이블 초기화, table.clear()는 헤더 삭제
        
        for item in event_list:
            row_position = self.tablewidget_event_list.rowCount()
            self.tablewidget_event_list.insertRow(row_position)
            self.tablewidget_event_list.setItem(row_position, 0, QTableWidgetItem(item.logic_name))
        header = self.tablewidget_event_list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch) # 열 너비를 현재 창 크기에 맞게 균등 조정   

    def add_event_clicked(self):
        
        self.event_add_widget = EventLogicAddDialog(self)
        self.event_add_widget.event_added.connect(self.load_evnt_data)
        self.event_add_widget.show()
        
    def delete_event_clicked(self):
        # QTableWidget에서 선택된 행들 가져오기
        selected_items = self.tablewidget_event_list.selectedItems()
        if not selected_items:
            return
        
        # 선택된 행 번호들을 중복 제거하여 수집
        selected_rows = list(set(item.row() for item in selected_items))
        
        # 선택된 행들의 이벤트 이름을 먼저 수집
        events_to_delete = []
        for row in selected_rows:
            event_name_item = self.tablewidget_event_list.item(row, 0)
            if event_name_item:
                events_to_delete.append(event_name_item.text())
        
        # DB에서 삭제
        for event_name in events_to_delete:
            try:
                self.get_db_logic_list.delete(logic_name=event_name)
                print(f"Deleted event '{event_name}' from database")
            except Exception as e:
                print(f"Failed to delete event '{event_name}' from database: {e}")
        
        # UI에서 삭제 (역순으로 삭제하여 인덱스 문제 방지)
        for row in sorted(selected_rows, reverse=True):
            self.tablewidget_event_list.removeRow(row)
    def load_evnt_data(self):

        logic_items = self.get_db_logic_list.select()
        
        # logic_name 기준으로 오름차순 정렬
        logic_items.sort(key=lambda logic: logic.logic_name)
        
        # 테이블 초기화
        self.tablewidget_event_list.setRowCount(0)
        
        # LogicList의 모든 항목을 테이블에 추가
        for logic in logic_items:
            self.add_event_to_table(logic.logic_name)
    
    def add_event_to_table(self, event_name):
        # 테이블에 이벤트 추가
        row_position = self.tablewidget_event_list.rowCount()
        self.tablewidget_event_list.insertRow(row_position)
        self.tablewidget_event_list.setItem(row_position, 0, QTableWidgetItem(event_name))
    
    def edit_event_content(self, row, column):
       
        # Get the event name from the selected row
        event_name_item = self.tablewidget_event_list.item(row, 0)
        if not event_name_item:
            return

        event_name = event_name_item.text()

        # Fetch the corresponding data from LogicList
    
        logic_items = self.get_db_logic_list.select(logic_name=event_name)

        if not logic_items:
            return
        

        logic_item = logic_items[0]  # Assuming unique logic_name
        self.event_edit_widget = EventLogicAddDialog(self)
        self.event_edit_widget.line_edit_event_name.setText(logic_item.logic_name)
        self.event_edit_widget.spinbox_skip_frame.setValue(int(logic_item.skip_frame))
        self.event_edit_widget.line_edit_input_img_size.setText(",".join(map(str, logic_item.input_img_size)))
        self.event_edit_widget.radio_danger_lowlow.setChecked(True) if logic_item.risk_level == 0 else self.event_edit_widget.radio_danger_low.setChecked(True) if logic_item.risk_level == 1 else self.event_edit_widget.radio_danger_mid.setChecked(True) if logic_item.risk_level == 2 else self.event_edit_widget.radio_danger_high.setChecked(True) if logic_item.risk_level == 3 else self.event_edit_widget.radio_danger_highhigh.setChecked(True)
        self.event_edit_widget.radio_left.setChecked(True) if logic_item.jiguk_direction == 1 else self.event_edit_widget.radio_right.setChecked(True) if logic_item.jiguk_direction == 2 else self.event_edit_widget.radio_top_side.setChecked(True) if logic_item.jiguk_direction == 3 else self.event_edit_widget.radio_under_side.setChecked(True) if logic_item.jiguk_direction == 4 else None
        self.event_edit_widget.edit_to_list(logic_item.logicListData)

        self.old_logic_name=logic_item.logic_name

        self.event_edit_widget.button_add_event_data.clicked.disconnect() # 기존의 "추가" 버튼 이벤트 연결 해제, insert 이 아닌 update 하기 위함.
        self.event_edit_widget.button_add_event_data.clicked.connect(lambda: self.update_logic_to_db())

        self.event_edit_widget.show()
        
    def update_logic_to_db(self):
        """
        Update the existing logic entry in the database.
        """
        if not self.event_edit_widget:
            return


        logic_name = self.event_edit_widget.line_edit_event_name.text().strip()
        
        # 업데이트할 값들
        skip_frame = int(self.event_edit_widget.spinbox_skip_frame.value())
        input_img_size = self.event_edit_widget.line_edit_input_img_size.text()
        logic_list_data = self.event_edit_widget.logic_list_data_arr
        risk_level_status = 0 if self.event_edit_widget.radio_danger_lowlow.isChecked() else 1 if self.event_edit_widget.radio_danger_low.isChecked() else 2 if self.event_edit_widget.radio_danger_mid.isChecked() else 3 if self.event_edit_widget.radio_danger_high.isChecked() else 4 if self.event_edit_widget.radio_danger_highhigh.isChecked() else 8
        jiguk_direction = 1 if self.event_edit_widget.radio_left.isChecked() else 2 if self.event_edit_widget.radio_right.isChecked() else 3 if self.event_edit_widget.radio_top_side.isChecked() else 4 if self.event_edit_widget.radio_under_side.isChecked() else 0
        
        # Update the database
        self.get_db_logic_list.update(
            old_logic_name=self.old_logic_name,
            logic_name = logic_name,  
            skip_frame = skip_frame, 
            input_img_size = input_img_size, 
            logicListData = logic_list_data,
            risk_level = risk_level_status,
            jiguk_direction = jiguk_direction
        ) 
        if self.old_logic_name != logic_name:
            self.cctv_list.change_unsafe_event_name(
                old_logic_name=self.old_logic_name,
                logic_name=logic_name
            )
            self.cctv_setting.change_unsafe_event_name(
                old_logic_name=self.old_logic_name,
                logic_name=logic_name
            )
        # Refresh the EventList table
        self.load_evnt_data()
        self.event_edit_widget.close()
        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = EventLogicManagementWidget()
    window.show()
    sys.exit(app.exec())