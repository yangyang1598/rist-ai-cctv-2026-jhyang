import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt  # plt 임포트 추가
import numpy as np

from ui.ui_login_dialog import Ui_Dialog

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout
from PySide6.QtCore import Qt


class LoginDialog(QDialog,Ui_Dialog):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("로그인")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginDialog()
    window.show()
    sys.exit(app.exec())