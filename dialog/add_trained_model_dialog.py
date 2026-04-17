from PySide6.QtWidgets import QDialog
from ui.ui_add_trained_model_dialog import Ui_Dialog
import matplotlib.pyplot as plt

# 2025.05.21 파일 추가 (박보은)
class AddTrainedModelDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # UI 설정
        self.setWindowTitle(f"모델 등록")
        
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'  # 대체 폰트 설정
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지