import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

import db.db_cctv_list as db_cctv_list
import db.db_logic_list as db_logic_list

from PySide6.QtWidgets import QWidget, QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal, Qt
from natsort import natsorted
from collections import defaultdict

from ui.ui_cctv_list_widget import Ui_Widget
from widget.video_process_pipeline.video_config import VideoConfig

class CctvListWidget(QWidget, Ui_Widget):
    stream_info_selected = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tree_widget_cctv_list.itemClicked.connect(self.on_item_clicked)
        self.button_cctv_search.clicked.connect(self.filter_tree_items)
        self.line_edit_cctv_search.returnPressed.connect(self.filter_tree_items)

        self.load_cctv_list_to_tree(self.tree_widget_cctv_list)

    def load_cctv_list_to_tree(self, tree_widget: QTreeWidget):
        rows = db_cctv_list.get_cctv_list()

        # 1. 자연 정렬을 위해 장소별 CCTV 저장
        location_dict = defaultdict(list)
        for row in rows:
            location_dict[row['camera_location']].append(row)

        # 2. 장소명 자연 정렬
        sorted_locations = natsorted(location_dict.keys())

        tree_widget.clear()

        for location in sorted_locations:
            location_item = QTreeWidgetItem([location])
            tree_widget.addTopLevelItem(location_item)

            # 3. CCTV 자연 정렬
            cctv_list = natsorted(location_dict[location], key=lambda r: r['camera_name'])
            for cctv in cctv_list:
                cctv_item = QTreeWidgetItem([cctv['camera_name']])
                cctv_item.setData(0, Qt.UserRole, cctv)
                location_item.addChild(cctv_item)

    def on_item_clicked(self, item, column):
        if item.parent() is not None:
            data = item.data(0, Qt.ItemDataRole.UserRole)
            cctv_info = self._create_cctv_info(data)
            self.stream_info_selected.emit(cctv_info)

    def _create_cctv_info(self, data):
        """CCTV 정보를 생성하는 공통 함수"""
        # RTSP URL 생성
        login_info = ""
        if data['rtsp_id'] and data['rtsp_pw']:
            login_info = f"{data['rtsp_id']}:{data['rtsp_pw']}@"
        
        stream_path = ""
        if data['stream_path']:
            stream_path = f"/{data['stream_path']}"
        
        stream_url = f"rtsp://{login_info}{data['camera_ip']}:{data['port']}{stream_path}"
        
        # 이벤트 정보 처리
        event = []
        if data.get('unsafe_event'):
            rows = db_logic_list.get_event_logic_by_logic_name(data['unsafe_event'].split(', '))
            for row in rows:
                json_data = json.loads(row['logicListData'])
                models = []
                
                for _data in json_data:
                    try:
                        model = {
                            "type": _data['type'],
                            "name": _data['model'] if _data['type'] == "AI" else _data['name'],
                            "class_name": _data['object'],
                            "class_index": _data['object_index']
                        }
                        models.append(model)
                    except:
                        pass
                
                info = {
                    "name": row["logic_name"],
                    "skip_frame": row["skip_frame"],
                    "input_img_size": row['input_img_size'],
                    "models": models,
                    "risk_level": row["risk_level"]
                }
                event.append(info)
        
        # cctv_info 딕셔너리 생성
        return {
            "is_visualize": True,
            "stream_info": {
                "camera_ip": data['camera_ip'],
                "camera_location": data['camera_location'],
                "camera_name": data['camera_name'],
                "rtsp_id": data['rtsp_id'],
                "rtsp_pw": data['rtsp_pw'],
                "id": data['id'],
                "port": data['port'],
                "ptz_port": data['ptz_port'],
                "protocol": data['protocol'],
                "stream_url": stream_url,
            },
            "events": event
        }

    def filter_tree_items(self):
        keyword = self.line_edit_cctv_search.text().strip().lower()

        for i in range(self.tree_widget_cctv_list.topLevelItemCount()):
            location_item = self.tree_widget_cctv_list.topLevelItem(i)
            any_visible = False

            for j in range(location_item.childCount()):
                cctv_item = location_item.child(j)
                name = cctv_item.text(0).lower()

                if keyword == "":
                    match = True
                else:
                    match = keyword in name

                cctv_item.setHidden(not match)
                if match:
                    any_visible = True

            location_item.setHidden(not any_visible)

    def get_all_items_info(self):
        cctv_info_list = []

        for i in range(self.tree_widget_cctv_list.topLevelItemCount()):
            location_item = self.tree_widget_cctv_list.topLevelItem(i)
            
            for j in range(location_item.childCount()):
                cctv_item = location_item.child(j)
                data = cctv_item.data(0, Qt.ItemDataRole.UserRole)
                cctv_info = self._create_cctv_info(data)
                cctv_info_list.append(cctv_info)
        
        return cctv_info_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CctvListWidget()
    widget.show()  
    sys.exit(app.exec()) 
