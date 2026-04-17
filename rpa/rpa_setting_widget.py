import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import*  # QFileDialog 추가
from PySide6.QtCore import *
from PySide6.QtGui import QCloseEvent

from rpa.ui.ui_RpaSettingWidget import Ui_RpaSettingWidget
from rpa.rpa_report_detail_dialog import RpaReportDetailDialog


class RpaSettingWidget(QWidget, Ui_RpaSettingWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("RPA Email")
        
        # 버튼 클릭 이벤트 연결
        


  


    def closeEvent(self, event: QCloseEvent) -> None:
        print("RPA Report Widget : closeEvent")
        # self.parent().show()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpaSettingWidget()
    window.show()
    sys.exit(app.exec())