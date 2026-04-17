import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import*  # QFileDialog 추가
from PySide6.QtCore import *
from PySide6.QtGui import QCloseEvent

from rpa.ui.ui_RpaHomeWidget import Ui_RpaHomeWidget
from rpa.rpa_report_detail_dialog import RpaReportDetailDialog


class RpaHomeWidget(QWidget, Ui_RpaHomeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("RPA Home")
        
        # 버튼 클릭 이벤트 연결
        # self.pushButton_report_new_manual.clicked.connect(self.btn_report_new_manual_clicked)
        # self.pushButton_report_new_event.clicked.connect(self.btn_report_new_event_clicked)



    def closeEvent(self, event: QCloseEvent) -> None:
        print("RPA Home Widget : closeEvent")
        # self.parent().show()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpaHomeWidget()
    window.show()
    sys.exit(app.exec())