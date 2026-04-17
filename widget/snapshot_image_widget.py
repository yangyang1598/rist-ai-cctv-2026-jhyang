
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db.db_ai_event_log as db_ai_event_log

from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QSizePolicy

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

from ui.ui_snapshot_image_widget import Ui_Widget
from dialog.ai_event_log_image_popup_dialog import AiEventLogImagePopupDialog

class ClickableLabel(QLabel):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.original_pixmap = QPixmap(image_path)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 최소 크기를 아주 작게 설정하여 5x5 그리드 안에서 자유롭게 조절되도록 함
        # self.setMinimumSize(100, 100) 

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_pixmap()

    def update_pixmap(self):
        if not self.original_pixmap.isNull():
            # 라벨의 현재 크기에 맞춰 스케일링 (비율 유지)
            size = self.size()
            if size.width() > 0 and size.height() > 0:
                scaled_pixmap = self.original_pixmap.scaled(
                    size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             popup = AiEventLogImagePopupDialog(self.image_path)
#             popup.exec()

class SnapshotImageWidget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.layout = QGridLayout()
        self.layout.setSpacing(5)  # 이미지 간 간격
        self.layout.setContentsMargins(5, 5, 5, 5) # 외곽 여백
        self.layout.setAlignment(Qt.AlignTop) # 상단 정렬
        self.columns = 5

        # 리사이징 지연 처리를 위한 타이머
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.update_image_sizes)

        # 모든 열의 너비를 동일하게 배분
        for i in range(self.columns):
            self.layout.setColumnStretch(i, 1)

        # 가로 스크롤 방지 및 세로 스크롤만 허용
        self.scroll_area_event_log_image.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_event_log_image.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.load_event_logs_image_to_scroll_area()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 위젯 크기가 바뀔 때 즉시 계산하지 않고, 레이아웃이 안정될 때까지 대기 후 처리
        self.resize_timer.start(50) 

    def showEvent(self, event):
        super().showEvent(event)
        # 위젯이 다시 보여질 때(사이드바 변경 등) 크기를 재계산
        QTimer.singleShot(50, self.update_image_sizes)

    def update_image_sizes(self):
        # 뷰포트 높이에서 여백과 간격을 제외한 값을 5로 나누어 한 이미지의 높이를 결정
        viewport_height = self.scroll_area_event_log_image.viewport().height()
        viewport_width = self.scroll_area_event_log_image.viewport().width()
        print(f"viewport_height: {viewport_height}, viewport_width: {viewport_width}")
        # 뷰포트 높이가 아직 0이거나 너무 작은 경우 (초기 렌더링 전) 계산 스킵
        if viewport_height < 50 or viewport_width < 50:
            return

        margins = self.layout.contentsMargins()
        spacing = self.layout.spacing()
        
        # 가시 영역에 5개가 들어오도록 높이 계산 (여백 2개 + 간격 4개 제외)
        available_height = viewport_height - (margins.top() + margins.bottom()) - (spacing * 4)
        available_width = viewport_width - (margins.left() + margins.right()) - (spacing * 4)
        
        target_height = max(10, available_height // 5)
        target_width = max(10, available_width // 5)

        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                # 모든 이미지 위젯의 높이를 고정하여 5x5 그리드 유지
                widget.setFixedHeight(target_height)
                widget.setFixedWidth(target_width)
                # 이미지 자체 업데이트 (라벨 크기 변경 대응)
                if hasattr(widget, 'update_pixmap'):
                    widget.update_pixmap()

    def load_event_logs_image_to_scroll_area(self):

        image_paths = db_ai_event_log.get_ai_event_logs(fields="image", limit=100)

        for i, item in enumerate(image_paths):
            path = item['image']  # 'image' 키에서 문자열 꺼내기

            label = ClickableLabel(path)
            if label.original_pixmap.isNull():
                label.setText("불러오기 실패")

            row = i // self.columns
            col = i % self.columns
            self.layout.addWidget(label, row, col)

        container_widget = QWidget()
        container_widget.setLayout(self.layout)

        self.scroll_area_event_log_image.setWidgetResizable(True)
        self.scroll_area_event_log_image.setWidget(container_widget)
        
        # 초기 로드 후 크기 업데이트 (UI가 완전히 그려진 후 계산되도록 지연 호출)
        QTimer.singleShot(10, self.update_image_sizes)

    def add_event_log_image_to_scroll_area(self, image_path):
        # 모든 위젯 리스트업
        widgets = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item and item.widget():
                widgets.append(item.widget())

        # 100개 초과 시 마지막 위젯 제거
        if len(widgets) >= 100:
            last_widget = widgets.pop()
            self.layout.removeWidget(last_widget)
            last_widget.deleteLater()

        # 새로운 위젯 생성
        new_label = ClickableLabel(image_path)
        if new_label.original_pixmap.isNull():
            new_label.setText("불러오기 실패")

        # 기존 위젯들 레이아웃에서 제거 (참조는 유지)
        for w in widgets:
            self.layout.removeWidget(w)

        # 새로운 위젯을 0번(가장 앞)에 추가
        widgets.insert(0, new_label)

        # 다시 레이아웃에 배치 (5열 기준)
        for i, w in enumerate(widgets):
            row = i // self.columns
            col = i % self.columns
            self.layout.addWidget(w, row, col)
            
        # 새로 추가된 위젯 포함하여 크기 업데이트
        self.update_image_sizes()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SnapshotImageWidget()
    widget.show()  
    sys.exit(app.exec()) 