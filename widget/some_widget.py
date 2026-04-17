import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal

class SomeWidget(QWidget):
    # 시그널 정의
    button_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("버튼을 눌러보세요.", self)
        self.button = QPushButton("클릭", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 시그널과 슬롯 연결
        self.button.clicked.connect(self.on_button_clicked)
        self.button_clicked.connect(self.update_label)

    def on_button_clicked(self):
        # 시그널 발생
        self.button_clicked.emit("버튼이 클릭되었습니다!")

    def update_label(self, text):
        self.label.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SomeWidget()
    # window.demo_data()

    window.show()
    sys.exit(app.exec())
