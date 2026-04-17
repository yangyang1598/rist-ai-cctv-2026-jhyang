import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import Qt
# Setting 클래스 임포트
from setting.use_qsetting import Setting


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ui_Dialog 임포트
from ui.ui_auto_delete_setting_dialog import Ui_Dialog

# 다이얼로그 클래스
class AutoDeleteSettingDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("자동정리 설정")
    
        # Setting 객체 생성
        self.setting = Setting("global_setting.ini")
        
        # 먼저 스핀박스의 최대값을 설정
        self.spinbox_required_capacity.setMaximum(10000)
        self.spinbox_delete_capacity.setMaximum(200)
        
        # 설정에서 값 가져오기
        required_capacity_str = self.setting.get("required_capacity", "100", group="자동 정리 설정")
        delete_capacity_str = self.setting.get("delete_capacity", "100", group="자동 정리 설정")
        
        try:
            required_capacity = int(required_capacity_str)
            delete_capacity = int(delete_capacity_str)
            print(f"로드된 값: required_capacity={required_capacity}, delete_capacity={delete_capacity}")
        except (ValueError, TypeError) as e:
            logger.error(f"설정값 변환 오류: {e}")
            required_capacity = 100
            delete_capacity = 100
    
        # UI 초기화 - 스핀박스 값 설정 (최대값 설정 후에!)
        self.spinbox_delete_capacity.setValue(delete_capacity)
        self.spinbox_required_capacity.setValue(required_capacity)
    
        # 설정 후 값 확인
        print(f"스핀박스에 설정된 값: required={self.spinbox_required_capacity.value()}, delete={self.spinbox_delete_capacity.value()}")
    
        # 버튼 시그널 연결
        self.button_apply_setting.clicked.connect(self.save_setting_value)
        
    def save_setting_value(self):
        # 스핀박스에서 값 가져오기
        required_capacity = self.spinbox_required_capacity.value()
        delete_capacity = self.spinbox_delete_capacity.value()
        
        try:
            # 값 설정 - group 파라미터를 사용하여 섹션 지정
            self.setting.set("required_capacity", str(required_capacity), group="자동 정리 설정")
            self.setting.set("delete_capacity", str(delete_capacity), group="자동 정리 설정")
            
            logger.info(f"자동 정리 설정이 업데이트되었습니다: required_capacity={required_capacity}, delete_capacity={delete_capacity}")
            self.accept()  # 다이얼로그 닫기
            
        except Exception as e:
            logger.error(f"설정 저장 중 오류 발생: {e}")
            self.reject()  # 오류 발생 시 다이얼로그 취소
            

# 테스트 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AutoDeleteSettingDialog()
    dialog.show()
    sys.exit(app.exec())
