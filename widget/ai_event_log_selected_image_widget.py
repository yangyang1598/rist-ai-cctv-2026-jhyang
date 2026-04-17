import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ui.ui_ai_event_log_selected_image_widget import Ui_Widget

class AiEventLogSelectedImageWidget(QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # UI 설정

    def set_event_log_info(self, event_log_info):
        print(event_log_info)

        # 이미지 사이즈 조정을 위해 사용
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label_image.setSizePolicy(size_policy)
        self.original_pixmap = None
        pixmap = QPixmap(event_log_info['image'])
        if pixmap.isNull():
            self.label_image.setText("이미지 불러오기 실패")
        else:
            self.original_pixmap = pixmap
            self.update_pixmap()

        self.label_location.setText(f"[ {event_log_info['cctv_location']} - {event_log_info['cctv_id']} ]")
        self.label_date.setText(f"{event_log_info['date']}")
        self.label_event.setText(f"{event_log_info['content']}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_pixmap()

    def update_pixmap(self):
        if self.original_pixmap:
            label_size = self.label_image.size()
            scaled_pixmap = self.original_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_image.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogSelectedImageWidget()
    widget.show()  
    sys.exit(app.exec()) 