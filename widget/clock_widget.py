import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtCore import QTimer, QTime, QDate, Qt
from PySide6.QtGui import QFont

class ClockWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Arial", 18))
        # self.setStyleSheet("color: navy;")
        self.setAlignment(Qt.AlignCenter)

        # 타이머로 매초 갱신
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.setText(f"[ {current_date} {current_time} ]")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ClockWidget()
    widget.show()  
    sys.exit(app.exec()) 
