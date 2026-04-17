import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.db_cctv_list as db_cctv_list

from PySide6.QtWidgets import QWidget, QApplication, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, Qt, QItemSelectionModel, QModelIndex
from natsort import natsorted
from collections import defaultdict

from ui.ui_ai_event_log_search_cctv_list_widget import Ui_Widget

class AiEventLogSearchCctvListWidget(QWidget, Ui_Widget):
    selected_cctv_changed = Signal(list)  # 선택된 아이템 변경 시그널
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # UI 설정
        self.setup_ui()
        self.init_ui()
        
    def setup_ui(self):
        self.model = QStandardItemModel()
        self.tree_view_cctv_list.header().hide()
        self.selected_item=set()

    def init_ui(self):
        self.tree_view_cctv_list.clicked.connect(self.on_clicked)
        self.button_cctv_search.clicked.connect(self.filter_tree_items)
        self.line_edit_cctv_search.returnPressed.connect(self.filter_tree_items)

        self.load_cctv_list_to_tree(self.tree_view_cctv_list)

    def load_cctv_list_to_tree(self, tree_view: QTreeView):
        rows = db_cctv_list.get_cctv_list()

        # 1. 자연 정렬을 위해 장소별 CCTV 저장
        location_dict = defaultdict(list)
        for row in rows:
            location_dict[row['camera_location']].append(row)

        # 2. 장소명 자연 정렬
        sorted_locations = natsorted(location_dict.keys())

        self.model.removeRows(0, self.model.rowCount())  # 기존 모델 초기화

        for location in sorted_locations:
            location_item = QStandardItem(location)
            location_item.setEditable(False)

            # 3. CCTV 자연 정렬
            cctv_list = natsorted(location_dict[location], key=lambda r: r['camera_name'])
            for cctv in cctv_list:
                cctv_item = QStandardItem(cctv['camera_name'])
                cctv_item.setEditable(False)
                cctv_item.setData(cctv, Qt.UserRole)
                location_item.appendRow(cctv_item)

            self.model.appendRow(location_item)

        tree_view.setModel(self.model)
        tree_view.expandAll()

    def on_clicked(self, index):
        tree_view = self.tree_view_cctv_list
        model = tree_view.model()
        item = model.itemFromIndex(index)
        
        if item is None:
            return

        selection_model = tree_view.selectionModel()

        if item.rowCount() == 0:
            if selection_model.isSelected(index):
                selection_model.select(index, QItemSelectionModel.Deselect)
                self.selected_item.remove(item.text())
            else:
                selection_model.select(index, QItemSelectionModel.Select)
                self.selected_item.add(item.text())

            # 자식 토글 후 부모 선택 상태도 업데이트
            parent = item.parent()
            if parent is not None:
                all_siblings_selected = True
                for i in range(parent.rowCount()):
                    sibling_index = parent.child(i).index()
                    if not selection_model.isSelected(sibling_index):
                        all_siblings_selected = False
                        break

                parent_index = parent.index()
                if all_siblings_selected:
                    selection_model.select(parent_index, QItemSelectionModel.Select)
                else:
                    selection_model.select(parent_index, QItemSelectionModel.Deselect)

        elif tree_view.isExpanded(index):  # 부모 아이템이면
            all_selected = True
            for i in range(item.rowCount()):
                child_index = item.child(i).index()
                if not selection_model.isSelected(child_index):
                    all_selected = False
                    break

            parent_index = item.index()
            if all_selected:
                # 모두 선택되어 있으면 모두 해제 & 부모도 해제
                for i in range(item.rowCount()):
                    child_index = item.child(i).index()
                    self.selected_item.remove(item.child(i).text())
                    selection_model.select(child_index, QItemSelectionModel.Deselect)
                selection_model.select(parent_index, QItemSelectionModel.Deselect)
            else:
                # 하나라도 선택 안 되어 있으면 모두 선택 & 부모도 선택
                for i in range(item.rowCount()):
                    child_index = item.child(i).index()
                    self.selected_item.add(item.child(i).text())
                    selection_model.select(child_index, QItemSelectionModel.Select)
                selection_model.select(parent_index, QItemSelectionModel.Select)
        self.selected_cctv_changed.emit(list(self.selected_item))  # 선택된 CCTV 목록 시그널 발송
    
    def filter_tree_items(self):
        tree_view = self.tree_view_cctv_list
        keyword = self.line_edit_cctv_search.text().strip().lower()
        model = tree_view.model()

        # 최상위 아이템 수 만큼 반복
        for i in range(model.rowCount()):
            location_item = model.item(i)
            any_visible = False

            # 각 location_item의 자식들 검사
            for j in range(location_item.rowCount()):
                cctv_item = location_item.child(j)
                name = cctv_item.text().lower()

                if keyword == "":
                    match = True
                else:
                    match = keyword in name

                # QTreeView에서 해당 행 숨기기/보이기
                cctv_index = cctv_item.index()
                tree_view.setRowHidden(cctv_index.row(), location_item.index(), not match)

                if match:
                    any_visible = True

            # location_item(부모 노드) 숨기기/보이기
            tree_view.setRowHidden(i, QModelIndex(), not any_visible)

    def get_selected_items_dict(self):
        selection_model = self.tree_view_cctv_list.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        model = self.tree_view_cctv_list.model()
        result = {}

        # 처리한 인덱스 중복 방지
        processed = set()

        for index in selected_indexes:
            if index.column() != 0:
                continue
            if index in processed:
                continue

            item = model.itemFromIndex(index)
            if item is None:
                continue

            parent = item.parent()

            if parent is None:
                # 부모 아이템 선택됨
                parent_name = item.text()
                result[parent_name] = {
                    "selected": True,
                    "children": ['all']
                }

                # 자식들도 처리된 걸로 표시
                for i in range(item.rowCount()):
                    processed.add(item.child(i).index())
            else:
                parent_name = parent.text()
                # 부모가 이미 selected=True면 자식 추가 안 함
                if parent_name in result and result[parent_name]["selected"] is True:
                    # 이미 부모 선택 상태이므로 자식 무시
                    pass
                else:
                    # 부모가 아직 등록 안 됐으면 초기화
                    if parent_name not in result:
                        result[parent_name] = {
                            "selected": False,
                            "children": []
                        }
                    result[parent_name]["children"].append(item.text())

            processed.add(index)
        print(result)
        return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogSearchCctvListWidget()
    widget.show()  
    sys.exit(app.exec()) 