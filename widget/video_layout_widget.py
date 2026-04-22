import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

import db.db_video_layout as db_video_layout

from PySide6.QtWidgets import QWidget, QApplication, QListWidget, QListWidgetItem, QInputDialog, QMessageBox, QLayoutItem
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QIcon
from ui.ui_video_layout_widget import Ui_Widget
from widget.video_process_pipeline.video_player_widget import VideoPlayerWidget
from widget.video_process_pipeline.video_config import VideoConfig, LayoutData, setup_logger


class VideoLayoutWidget(QWidget, Ui_Widget):
    grid_data = Signal(dict)

    def __init__(self, video_player_widget=None):
        super().__init__()
        self.logger = setup_logger("VideoLayoutWidget")
        self.setupUi(self)
        
        # 버튼 아이콘 경로를 절대 경로로 재설정
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.button_add_video_layout.setIcon(QIcon(os.path.join(base_dir, 'src', 'icon', 'video_layout_add.svg')))
        self.button_edit_video_layout.setIcon(QIcon(os.path.join(base_dir, 'src', 'icon', 'video_layout_edit.svg')))
        self.button_delete_video_layout.setIcon(QIcon(os.path.join(base_dir, 'src', 'icon', 'video_layout_delete.svg')))
        
        self.video_player_widget: VideoPlayerWidget = video_player_widget
        self.current_layout_data: LayoutData = LayoutData()
        if self.video_player_widget:
            self.video_player_widget.current_layout_data.connect(self.on_current_layout_data)

        self.button_add_video_layout.clicked.connect(self.add_video_layout)
        self.button_delete_video_layout.clicked.connect(self.delete_video_layout)
        self.list_widget_video_layout.itemDoubleClicked.connect(self.on_item_clicked)

        self.load_video_layouts_to_list(self.list_widget_video_layout)

    def load_video_layouts_to_list(self, list_widget: QListWidget):
        list_widget.clear()

        rows = db_video_layout.get_video_layouts()
        for row in rows:
            layout_item = QListWidgetItem(row['name'])
            layout_item.setData(Qt.ItemDataRole.UserRole, row)
            list_widget.addItem(layout_item)
        
    def add_video_layout(self):
        # 팝업으로 레이아웃 이름 입력받기
        text, ok = QInputDialog.getText(self, "레이아웃 이름", "새 레이아웃 이름을 입력하세요:")
        if ok:
            if text.strip():
                layout_name = text.strip()

                if self.video_player_widget:
                    new_video_data = self.find_grid_layout()
                    self.save_video_layout(layout_name, new_video_data)
                else:
                    QMessageBox.warning(self, "오류", "비디오 플레이어 위젯이 초기화되지 않았습니다.")
            else:
                QMessageBox.warning(self, "입력 오류", "레이아웃 이름을 입력하지 않았습니다.")

    def find_grid_layout(self):
        self.video_player_widget.send_current_layout_data()
        grid_layout = self.video_player_widget.grid_layout
        cctv_info = self.current_layout_data.cctv_info
        new_video_data = []

        # 그리드 크기 정보 가져오기
        grid_row = self.video_player_widget.grid_row
        grid_col = self.video_player_widget.grid_col
        
        # 전체 그리드 위치를 추적하기 위한 딕셔너리
        occupied_positions = {}

        # cctv_info가 있는 경우 해당 위치들을 먼저 처리
        if cctv_info:
            # cctv_info 딕셔너리의 키들을 리스트로 변환하여 순회
            cctv_keys = list(cctv_info.keys())
            
            # 각 CCTV 정보에 대해 그리드 위치 확인
            for key in cctv_keys:
                if key in cctv_info:
                    # video_widgets에서 해당 키의 위젯 찾기
                    video_widget = self.video_player_widget.video_widgets.get(key)
                    if video_widget:
                        # 그리드에서 해당 위젯의 위치 찾기
                        widget_index = grid_layout.indexOf(video_widget)
                        if widget_index >= 0:
                            row, col, _, _ = grid_layout.getItemPosition(widget_index)
                            occupied_positions[(row, col)] = {
                                "position": [row, col],
                                "cctv_info": cctv_info[key].to_dict(),
                            }
        
        # 전체 그리드에 대해 순회하여 빈 칸은 빈 딕셔너리로 채우기
        for row in range(grid_row):
            for col in range(grid_col):
                if (row, col) in occupied_positions:
                    # 실제 비디오가 있는 위치
                    new_video_data.append(occupied_positions[(row, col)])
                else:
                    # 빈 위치에는 빈 딕셔너리 추가
                    new_video_data.append({
                        "position": [row, col],
                        "cctv_info": {},
                    })
        
        # 디버깅용 출력
        # for video_data in new_video_data:
        #     self.logger.debug(f"Position: {video_data['position']}, Stream URL: {video_data['stream_url']}")

        return new_video_data

    def save_video_layout(self, layout_name: str, video_data_list: list[dict]):
        video_data_json = json.dumps(video_data_list, ensure_ascii=False)
        if db_video_layout.add_video_layout(layout_name, video_data_json) > 0:
            layout_item = QListWidgetItem(layout_name)
            layout_item.setData(Qt.ItemDataRole.UserRole, {"name": layout_name, "video_data": video_data_json})
            self.list_widget_video_layout.addItem(layout_item)

    def update_video_layout(self, layout_name: str, video_data_list: list[dict]):
        video_data_json = json.dumps(video_data_list, ensure_ascii=False)
        if db_video_layout.update_video_layout_by_name(layout_name, video_data_json) > 0:
            for i in range(self.list_widget_video_layout.count()):
                item = self.list_widget_video_layout.item(i)
                if item.text() == layout_name:
                    updated_data = {"name": layout_name, "video_data": video_data_json}
                    item.setData(Qt.ItemDataRole.UserRole, updated_data)
                    break

    def delete_video_layout(self):
        selected_items = self.list_widget_video_layout.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "선택 오류", "삭제할 레이아웃을 선택하세요.")
            return

        for item in selected_items:
            layout_name = item.text()

            result = QMessageBox.question(
                self, "삭제 확인", f"선택한 {layout_name} 레이아웃을 삭제하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.Yes:
                # DB에서 삭제
                if db_video_layout.delete_video_layout_by_name(layout_name) > 0:
                        row = self.list_widget_video_layout.row(item)
                        self.list_widget_video_layout.takeItem(row)
                else:
                    # QMessageBox.critical(self, "삭제 실패", f"{layout_name} 레이아웃 삭제 실패")
                    pass
                    
    #region 모델학습 시 활성/비활성 레이아웃
    def add_model_video_layout(self, text: str):
        print(f"Adding model video layout with name: {text}")
        if text.strip():
            layout_name = text.strip()

            if self.video_player_widget:
                new_video_data = self.find_grid_layout()
                self.save_video_layout(layout_name, new_video_data)
            else:
                QMessageBox.warning(self, "오류", "비디오 플레이어 위젯이 초기화되지 않았습니다.")

    def delete_model_video_layout(self, layout_name: str):
        if layout_name.strip():
            if db_video_layout.delete_video_layout_by_name(layout_name) > 0:
                for i in range(self.list_widget_video_layout.count()):
                    item = self.list_widget_video_layout.item(i)
                    if item.text() == layout_name:
                        self.list_widget_video_layout.takeItem(i)
                        break
            else:
                #QMessageBox.critical(self, "삭제 실패", f"{layout_name} 레이아웃 삭제 실패")
                pass

    def find_layout_by_name(self, layout_name: str):
        """레이아웃 이름으로 해당 아이템을 찾아 데이터를 반환합니다."""
        for i in range(self.list_widget_video_layout.count()):
            item = self.list_widget_video_layout.item(i)
            if item.text() == layout_name:
                text = item.data(Qt.ItemDataRole.UserRole)
                data: dict = json.loads(text) if isinstance(text, str) else text
                self.grid_data.emit(data)  # 시그널로 데이터 전송
                return data
        return None
    #endregion
    
    @Slot(dict)
    def on_item_clicked(self, item: QListWidgetItem):
        text = item.data(Qt.ItemDataRole.UserRole)
        data: dict = json.loads(text) if isinstance(text, str) else text
        self.grid_data.emit(data)

    @Slot(LayoutData)
    def on_current_layout_data(self, layout_data: LayoutData):
        self.current_layout_data = layout_data  # 값을 저장

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = VideoLayoutWidget()
    widget.show()  
    sys.exit(app.exec()) 
