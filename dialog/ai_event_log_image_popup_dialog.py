import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class AiEventLogImagePopupDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(f"이미지 확인: {image_path}")
        self.resize(500, 400)

        self.original_pixmap = None
        self.label = QLabel("이미지 불러오는 중...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: #f0f0f0;")
        self.label.setScaledContents(False)

        # 이미지 사이즈 조정을 위해 사용
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setSizePolicy(size_policy)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.load_image_to_label(image_path)

    def load_image_to_label(self, image_path):
        if not os.path.exists(image_path):
            self.label.setText("이미지 파일이 존재하지 않습니다.")
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.label.setText("이미지를 불러올 수 없습니다.")
        else:
            self.original_pixmap = pixmap
            self.update_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_pixmap()

    def update_pixmap(self):
        if self.original_pixmap:
            label_size = self.label.size()
            scaled_pixmap = self.original_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = AiEventLogImagePopupDialog("img/20250527_194117_CCTV 100_HamanFall.jpeg")
    dlg.exec()
