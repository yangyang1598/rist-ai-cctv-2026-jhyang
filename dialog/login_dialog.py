import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt  # plt 임포트 추가
import numpy as np

from ui.ui_login_dialog import Ui_Dialog

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt

from db.db_accounts import DbAccounts

class LoginDialog(QDialog,Ui_Dialog):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("로그인")
        
        # 버튼 클릭 이벤트 연결
        self.button_login.clicked.connect(self.confirm_login_info)

    def confirm_login_info(self):
        # 입력된 아이디와 비밀번호 가져오기
        input_id = self.lineEdit_id.text().strip()
        input_pw = self.lineEdit_pw.text().strip()

        if not input_id or not input_pw:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호를 확인하세요")
            return

        # DB에서 해당 정보가 있는지 검증
        accounts = DbAccounts().select(user_id=input_id, user_password=input_pw)

        if accounts and len(accounts) > 0:
            QMessageBox.information(self, "로그인 성공", "로그인되었습니다")
            self.accept()  # 다이얼로그 닫기 (로그인 성공 처리)
        else:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호를 확인하세요")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginDialog()
    window.show()
    sys.exit(app.exec())