from PySide6.QtWidgets import QDialog, QFileDialog
from ui.ui_add_new_model_dialog import Ui_Dialog
import matplotlib.pyplot as plt
from pathlib import Path

# 2025.05.21 파일 추가 (박보은)
class AddNewModelDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # UI 설정
        self.setWindowTitle(f"모델 등록")

        # 데이터 설정 파일 경로 숨김
        self.label_dataset_config_file_path.setVisible(False)
        self.line_edit_dataset_config_file_path.setVisible(False)
        self.button_dataset_config_file_path.setVisible(False)
        
        self.button_model_file_path.setVisible(False)  # 모델 파일 경로 버튼 숨김
        
        self.button_model_file_path.clicked.connect(self.hendle_button_model_file_path_clicked)
        self.button_dataset_config_file_path.clicked.connect(self.hendle_button_dataset_config_file_path_clicked)

        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'  # 대체 폰트 설정
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

    def hendle_button_model_file_path_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "모델 파일 선택",  # 타이틀
            "",  # 기본 경로
            "Model Files (*.pt)"  # 필터
        )

        if file_path:
            self.line_edit_model_file_path.setText(file_path)
            if self.line_edit_model_name.text().strip() == "":
                file_name = Path(file_path)
                self.line_edit_model_name.setText(file_name.stem)

    def hendle_button_dataset_config_file_path_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "데이터 설정 파일 선택",  # 타이틀
            "",  # 기본 경로
            "YAML Files (*.yaml *.yml)"  # 필터
        )

        if file_path:
            self.line_edit_dataset_config_file_path.setText(file_path)

    def get_add_model_info(self):
        return (self.line_edit_model_description.text(), self.line_edit_model_name.text(), self.line_edit_model_file_path.text(), self.line_edit_dataset_config_file_path.text())

