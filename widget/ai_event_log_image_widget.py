
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db.db_ai_event_log as db_ai_event_log

from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QScrollArea

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ui.ui_ai_event_log_image_widget import Ui_Widget
from dialog.ai_event_log_image_popup_dialog import AiEventLogImagePopupDialog

class ClickableLabel(QLabel):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            popup = AiEventLogImagePopupDialog(self.image_path)
            popup.exec()

class AiEventLogImageWidget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.load_event_logs_image_to_scroll_area()


    def load_event_logs_image_to_scroll_area(self):

        image_paths = db_ai_event_log.get_ai_event_logs(fields="image", limit=100)

        for item in image_paths:
            path = item['image']  # 'image' 키에서 문자열 꺼내기

            label = ClickableLabel(path)
            label.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(path)

            if pixmap.isNull():
                label.setText("불러오기 실패")
            else:
                label.setPixmap(pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.layout.addWidget(label)

        container_widget = QWidget()
        container_widget.setLayout(self.layout)

        self.scroll_area_event_log_image.setWidgetResizable(True)
        self.scroll_area_event_log_image.setWidget(container_widget)

    def add_event_log_image_to_scroll_area(self, image_path):
        if self.layout.count() >= 100:
            last_item = self.layout.itemAt(self.layout.count() - 1)
            if last_item:
                last_widget = last_item.widget()
                if last_widget:
                    self.layout.removeWidget(last_widget)
                    last_widget.deleteLater()  # 메모리에서도 제거

        label = ClickableLabel(image_path)
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            label.setText("불러오기 실패")
        else:
            label.setPixmap(pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.layout.insertWidget(0, label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogImageWidget()
    widget.show()  
    sys.exit(app.exec()) 