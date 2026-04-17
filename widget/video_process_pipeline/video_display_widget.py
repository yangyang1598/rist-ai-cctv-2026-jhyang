# video_display_widget.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QImage, QPixmap, QMouseEvent, QPixmapCache
from widget.video_process_pipeline.video_config import VideoConfig
from rich.console import Console
console = Console()

class VideoDisplayWidget(QWidget):
    is_cctv_clicked = Signal(dict)
    is_cctv_double_clicked = Signal(dict)

    def __init__(self, video_id: int, cctv_info: VideoConfig, parent=None):
        super().__init__(parent)
        QPixmapCache.setCacheLimit(64 * 1024)  # 16MB (단위는 KB)
        self.video_id = video_id
        self.cctv_info = cctv_info
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.emit_single_click_info) # 단일 클릭 처리 함수 연결
        self._init_ui()

    def _init_ui(self):
        # 레이아웃 설정
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 비디오 라벨 - 프레임이 표시되는 곳
        self.video_label = QLabel()
        self.video_label.setScaledContents(False)
        self.video_label.setMinimumSize(1, 1)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_label)
    
    def update_frame(self, q_image: QImage):
        if q_image is None:
            return
        try:
            self.clear_display()

            # 셀 크기에 맞게 프레임을 QLabel에 꽉 채워서 표시 (aspect ratio 무시)
            label_width = self.video_label.width()
            label_height = self.video_label.height()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(
                label_width,
                label_height,
                Qt.AspectRatioMode.IgnoreAspectRatio,  # 비율 무시하고 꽉 채움
                Qt.TransformationMode.SmoothTransformation
            )
            self.video_label.setPixmap(scaled_pixmap)
            
            # self.pixmap = QPixmap.fromImage(q_image)
            # self.video_label.setPixmap(self.pixmap)
            del q_image
        except Exception as e:
            pass
    
    def clear_display(self):
        """디스플레이를 초기화합니다."""
        self.video_label.clear()
        if hasattr(self, "pixmap"):
            del self.pixmap

    def mousePressEvent(self, event: QMouseEvent):
        """
        마우스 클릭 이벤트 처리 - CCTV 정보 출력
        {
            "camera_ip": "192.168.88.174",
            "camera_location": "1공장",
            "camera_name": "CCTV 1",
            "id": 12,
            "port": 8554,
            "protocol": "TCP",
            "rtsp_id": "",
            "rtsp_pw": "",
            "skip_frame": 1,
            "stream_path": "test1",
            "stream_url": "rtsp://192.168.88.174:8554/test1",
            "unsafe_event": "사람 감지, 중량물 접근, 사람과 공"
        }
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_timer.start(QApplication.doubleClickInterval())

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """마우스 더블 클릭 이벤트 - 타이머 중지 및 더블 클릭 처리"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_timer.stop()
            self.is_cctv_double_clicked.emit(
                {
                "camera_id": self.cctv_info.camera_info["id"],
                "camera_name": self.cctv_info.camera_info["camera_name"],
                "video_num": self.video_id,
                "camera_ip": self.cctv_info.camera_info["camera_ip"],
                "port": self.cctv_info.camera_info["port"],
                "ptz_port": self.cctv_info.camera_info["ptz_port"],
                "rtsp_id": self.cctv_info.camera_info["rtsp_id"],
                "rtsp_pw": self.cctv_info.camera_info["rtsp_pw"]
                }
            ) 

    def emit_single_click_info(self):
        """타이머가 정상적으로 완료되었을 때 (더블 클릭이 아닐 때) 호출됨"""
        self.is_cctv_clicked.emit(
            {
                "camera_id": self.cctv_info.camera_info["id"],
                "camera_name": self.cctv_info.camera_info["camera_name"],
                # "video_num": self.cctv_info.video_number,
                "video_num": self.video_id,
                "camera_ip": self.cctv_info.camera_info["camera_ip"],
                "port": self.cctv_info.camera_info["port"],
                "ptz_port": self.cctv_info.camera_info["ptz_port"],
                "rtsp_id": self.cctv_info.camera_info["rtsp_id"],
                "rtsp_pw": self.cctv_info.camera_info["rtsp_pw"]
            }
        )