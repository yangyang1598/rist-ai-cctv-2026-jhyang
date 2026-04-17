import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.db_cctv_list as db_cctv_list

from widget.video_process_pipeline.video_process_manager import ProcessManager
from ui.ui_status_widget import Ui_Widget

from natsort import natsorted
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QFontMetrics

import math

class EventStatusFrame(QFrame):
    def __init__(self, cctv_location, cctv_name: str, status: bool, frame_size: tuple):
        super().__init__()

        self.location_name = f"{cctv_location} {cctv_name}"  # Store original text
        self.cctv_status = "-" if status else "오프라인"  # Store original status text

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(2, 2, 2, 2)

        self.label_name = QLabel(self.truncate_text(self.location_name, frame_size[0]))
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


        self.label_status = QLabel(self.truncate_text(self.cctv_status, frame_size[0]))
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label_status.setMaximumWidth(frame_size[0])

        self.label_name.setStyleSheet("border: none; background: none;")
        self.label_status.setStyleSheet("border: none; background: none;")

        layout.addWidget(self.label_name)
        layout.addWidget(self.label_status)

        self.setLayout(layout)

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(2)
        self.width, self.height = frame_size
        self.set_style_sheet("lightgreen" if status else "lightgray")

        self.risk_level = -1
        self.reset_timer = QTimer(self)
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.update_event_status)

    def truncate_text(self, text: str, max_width: int) -> str:
        font_metrics = QFontMetrics(self.font())
        max_width = max_width - 8
        if font_metrics.horizontalAdvance(text) > max_width:
            ellipsis = "..."
            while font_metrics.horizontalAdvance(text + ellipsis) > max_width and len(text) > 1:
                text = text[:-1]
            text = text + ellipsis if text else ""

        return text

    def set_style_sheet(self, color, risk_level: int=-1):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 1px solid gray;
                border-radius: 4px;
                padding: 1px;
                width: {self.width}px;
                height: {self.height}px;
            }}
        """)

    def update_cctv_status(self, status: bool):
        if status:
            if self.risk_level == -1:
                self.label_status.setText(self.truncate_text("-", self.width ))
                color = "lightgreen"
            else:
                return
        else:
            self.reset_timer.stop()
            self.risk_level = -1
            self.label_status.setText(self.truncate_text("오프라인", self.width ))
            color = "lightgray"

        self.set_style_sheet(color)

    def update_event_status(self, event_name="-", event_risk_level=-1,jiguk_performed=False,danger_maintain_time=30):
        if event_risk_level == -1:
            color = "lightgreen"
        elif event_risk_level == 0 and not jiguk_performed:
            color = "lightcoral"
        elif event_risk_level == 0 and jiguk_performed:
            color = "yellow"
        else:
            color = "orange"

        self.cctv_status = event_name
        self.label_status.setText(self.truncate_text(event_name, self.width - 4))
        self.set_style_sheet(color, risk_level=event_risk_level)

        self.risk_level = event_risk_level
        self.reset_timer.stop()
        self.reset_timer.start(int(danger_maintain_time) * 1000)

    def resizeEvent(self, event):
        """Handle frame resize by updating label text truncation."""
        super().resizeEvent(event)
        self.width = self.size().width()  # Update stored width
        
        new_width = self.width  # Adjust for margins
        self.label_name.setMaximumWidth(new_width)
        self.label_status.setMaximumWidth(new_width)
        self.label_name.setText(self.truncate_text(self.location_name, new_width))
        self.label_status.setText(self.truncate_text(self.cctv_status, new_width))

class CctvStatusFrame(QFrame):
    def __init__(self, cctv_location, cctv_name: str, status: bool, frame_size: tuple):
        super().__init__()

        self.location_text = f"{cctv_location} {cctv_name}"  # Store original text
        self.cctv_status = "온라인" if status else "오프라인"  # Store original status text

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(2, 2, 2, 2)

        self.label_name = QLabel(self.truncate_text(self.location_text, frame_size[0]- 4))
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


        self.label_status = QLabel(self.truncate_text(self.cctv_status, frame_size[0]- 4))
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label_status.setMaximumWidth(frame_size[0]- 4)

        self.label_name.setStyleSheet("border: none; background: none; ")
        self.label_status.setStyleSheet("border: none; background: none;")

        layout.addWidget(self.label_name)
        layout.addWidget(self.label_status)

        self.setLayout(layout)

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(2)
        self.width, self.height = frame_size
        self.set_style_sheet(status)

    def truncate_text(self, text: str, max_width: int) -> str:
        font_metrics = QFontMetrics(self.font())
        max_width = max_width - 8
        if font_metrics.horizontalAdvance(text) > max_width:
            ellipsis = "..."
            while font_metrics.horizontalAdvance(text + ellipsis) > max_width and len(text) > 1:
                text = text[:-1]
            text = text + ellipsis if text else ""

        return text

    def set_style_sheet(self, status):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'lightgreen' if status else 'lightgray'};
                border: 1px solid gray;
                border-radius: 4px;
                padding: 1px;
                width: {self.width}px;
                height: {self.height}px;
            }}
        """)

    def update_cctv_status(self, status: bool):
        self.cctv_status = "온라인" if status else "오프라인"
        self.label_status.setText(self.truncate_text(self.cctv_status, self.width ))
        self.set_style_sheet(status)

    def resizeEvent(self, event):
        """Handle frame resize by updating label text truncation."""
        super().resizeEvent(event)
        new_width = self.width   # Adjust for margins
        self.label_name.setMaximumWidth(new_width)
        self.label_status.setMaximumWidth(new_width)
        self.label_name.setText(self.truncate_text(self.location_text, new_width))
        self.label_status.setText(self.truncate_text(self.cctv_status, new_width))
        self.width = self.size().width()  # Update stored width

class StatusWidget(QWidget, Ui_Widget):
    def __init__(self, process_manager, widget_type):
        super().__init__()
        self.setupUi(self)

        self.process_manager: ProcessManager = process_manager
        self.widget_type = widget_type
        self.frame_map = {}  # (camera_name, camera_location) -> frame
        self.init_ui()

    def init_ui(self):
        cctvs = db_cctv_list.get_cctv_list('camera_location, camera_name')

        sorted_cctvs = natsorted(
            cctvs,
            key=lambda c: (c['camera_location'], c['camera_name'])
        )

        # cctv 갯수에 따른 동적 그리드 프레임 크기 계산
        total_cctvs = len(sorted_cctvs)
        columns = math.ceil(math.sqrt(total_cctvs))  # 정사각형에 가까운 그리드
        rows = math.ceil(total_cctvs / columns)
        if total_cctvs > 0:  # 0 나누기 방지
            #기본 위젯 크기 975 x 548 기준으로 프레임 크기 계산
            frame_width = (975 - (columns - 1) * 1) // columns
            frame_height = (548 - (rows - 1) * 1) // rows
        else:
            frame_width, frame_height = 50, 50  # 기본값

        frame_size = (frame_width, frame_height)

        self.layout_status.setContentsMargins(0, 0, 0, 0)
        self.layout_status.setSpacing(1)

        for index, cctv in enumerate(sorted_cctvs):
            row = index // columns
            col = index % columns

            key = (cctv['camera_name'], cctv['camera_location'])
            status = key in {
                (v['camera_name'], v['camera_location'])
                for v in self.process_manager.active_camera_list.values()
            }

            # 5. 프레임 생성 및 추가
            frame_cls = CctvStatusFrame if self.widget_type == 'cctv' else EventStatusFrame
            frame = frame_cls(cctv['camera_location'], cctv['camera_name'], status, frame_size)
            self.layout_status.addWidget(frame, row, col)

            # 6. 프레임 맵 저장
            self.frame_map[key] = frame

    def update_cctv_status(self):
        camera_info_source = self.process_manager.active_camera_list

        active_keys = set()
        for video_id, process in self.process_manager.processes.items():
            # 1. 프로세스가 살아있는지
            is_alive = process.is_alive()
            # 2. 정상 종료되지 않았는지
            is_not_terminated = process.exitcode is None
            # 3. 해당 video_id가 active_camera_list에 있는지
            has_info = video_id in camera_info_source
            # 4. 스트림이 정상인지
            is_healthy = self.process_manager.is_stream_healthy(video_id)
            
            # 네 조건을 모두 만족해야 온라인으로 간주
            if is_alive and is_not_terminated and has_info and is_healthy:
                camera_info = camera_info_source[video_id]
                key = (camera_info['camera_name'], camera_info['camera_location'])
                active_keys.add(key)

        for key, frame in self.frame_map.items():
            status = key in active_keys
            frame.update_cctv_status(status)

    def update_event_status(self, event_log):
        key = (event_log.cctv_name, event_log.cctv_location)
        frame = self.frame_map[key]
        frame.update_event_status(event_log.event_name, event_log.event_risk_level,event_log.jiguk_performed,event_log.danger_maintain_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = StatusWidget('1공장', 'CCTV 01', True)
    widget.show()  
    sys.exit(app.exec()) 
