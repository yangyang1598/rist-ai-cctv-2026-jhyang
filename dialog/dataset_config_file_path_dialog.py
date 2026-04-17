from PySide6.QtWidgets import QDialog, QFileDialog
from ui.ui_dataset_config_file_path_dialog import Ui_Dialog
import matplotlib.pyplot as plt

# 2025.05.21 파일 추가 (박보은)
class DatasetConfigFilePathDialog(QDialog, Ui_Dialog):
    def __init__(self, model_description, dataset_config_file_path=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # UI 설정
        self.setWindowTitle(f"데이터셋 경로 - {model_description}")
        
        # layout = QVBoxLayout(self)
        self.line_edit_dataset_config_file_path.setText(dataset_config_file_path)
        self.button_dataset_config_file_path_search.hide()  # 버튼 숨김 처리
        # self.button_dataset_config_file_path_search.clicked.connect(self.handle_dataset_config_file_path_search_clicked)

        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'  # 대체 폰트 설정
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

    def handle_dataset_config_file_path_search_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "데이터 설정 파일 선택",  # 타이틀
            "",  # 기본 경로
            "YAML Files (*.yaml *.yml);;All Files (*)"  # 필터
        )
        if file_path:
            self.line_edit_dataset_config_file_path.setText(file_path)

            
    def get_data_config_file_path(self):
        return self.line_edit_dataset_config_file_path.text()
