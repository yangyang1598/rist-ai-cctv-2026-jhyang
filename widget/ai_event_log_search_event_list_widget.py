import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.db_logic_list as db_logic_list

from PySide6.QtWidgets import QWidget, QApplication, QListView, QStyledItemDelegate, QStyleOptionButton, QStyle
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QRect, QModelIndex, QEvent
from ui.ui_ai_event_log_search_event_list_widget import Ui_Widget

class CheckBoxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = index.data(Qt.CheckStateRole)
        check_box_style_option = QStyleOptionButton()
        check_box_style_option.state |= QStyle.State_Enabled

        if value == Qt.Checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)

        # 체크박스 그리기
        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)
       
        # 텍스트 그리기
        text = index.data(Qt.DisplayRole)
        text_rect = QRect(
            check_box_style_option.rect.right() + 5,
            option.rect.top(),
            option.rect.width() - check_box_style_option.rect.width() - 10,
            option.rect.height()
        )
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)

    def editorEvent(self, event, model, option, index):
        return False    # 모든 이벤트 무시함 (Qt 기본동작도 무시함) : 체크박스 및 행 클릭 시 체크 상태 변경을 위해

    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        x = option.rect.x() + 5
        y = option.rect.y() + (option.rect.height() - check_box_rect.height()) // 2
        return QRect(x, y, check_box_rect.width(), check_box_rect.height())

class AiEventLogSearchEventListWidget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = QStandardItemModel()
        self.event_list = db_logic_list.get_event_logic_name()
        
        self.list_view_event_list.setModel(self.model)
        self.list_view_event_list.setItemDelegate(CheckBoxDelegate())

        self.load_event_list_to_list(self.event_list)
        self.list_view_event_list.clicked.connect(self.toggle_check_state)  
        self.button_event_search.clicked.connect(self.filter_list_items)
        
    def load_event_list_to_list(self, event_list):
        self.model.clear()

        # logic_name으로 정렬
        sorted_event_list = sorted(event_list, key=lambda x: x['logic_name'])
        
        for event in sorted_event_list:
            name = event['logic_name']
            item = QStandardItem(name)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)

    def toggle_check_state(self, index):
        current_state = self.list_view_event_list.model().data(index, Qt.CheckStateRole)
        new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
        self.list_view_event_list.model().setData(index, new_state, Qt.CheckStateRole)
    
    def filter_list_items(self):
        keyword = self.line_edit_event_search.text().strip()
        if keyword == "":
            self.load_event_list_to_list(self.event_list)
        else:
            filtered = [event for event in self.event_list if keyword in event['logic_name']]
            self.load_event_list_to_list(filtered)

    def get_selected_items_dict(self):
        result = []
        for row in range(self.model.rowCount()):
            check_item = self.model.item(row)
            if check_item.checkState() == Qt.Checked:
                result.append(check_item.text())
        return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogSearchEventListWidget()
    widget.show()  
    sys.exit(app.exec())   