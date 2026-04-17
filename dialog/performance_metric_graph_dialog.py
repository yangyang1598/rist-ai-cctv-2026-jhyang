import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt  # plt 임포트 추가
import numpy as np

from db.db_model_list import DbModelList

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6.QtCore import Qt


# 2025.05.19 파일 추가 (박보은)
class PerformanceMetricGraphDialog(QDialog):
    def __init__(self, model_description, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"성능지표 - {model_description}")
        self.setMinimumSize(800, 500)
        
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'  # 대체 폰트 설정
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
        
        layout = QVBoxLayout(self)

        # matplotlib Figure 생성
        fig = Figure(figsize=(5, 4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.db_model_list = DbModelList()
        model_metrics = self.db_model_list.select(model_description=model_description)[0]
        ax = fig.add_subplot(111)
        self.plot_metrics(ax, model_metrics, model_description)
        canvas.draw() 

    def plot_metrics(self, ax, model_metrics, model_description):
        labels = ['Precision', 'Recall', 'mAP@0.5', 'mAP@0.5:0.95', 'F1-Score', 'Speed']
        values = [model_metrics.precision, model_metrics.recall, model_metrics.map50, model_metrics.map50_95, model_metrics.f1_score, model_metrics.speed]
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#bcbd22', '#d62728', '#9467bd']
        max_val = max(values) * 1.1 if values else 1

        bars = ax.bar(labels, values, color=colors[:len(values)])
        ax.set_ylim(0, max_val)

        ax.set_title(f"{model_description} 모델 성능")
        ax.set_ylabel("값")
        ax.grid(axis='y', linestyle='--', alpha=0.6)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.02, f'{height:.2f}', ha='center')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PerformanceMetricGraphDialog()
    window.show()
    sys.exit(app.exec())