import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.db_ai_event_log as db_ai_event_log

from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import QDateTime, QDate, QTime, QThread, Signal, Slot, Qt, QRect, QEvent, QSize
from PySide6.QtGui import QMouseEvent
from ui.ui_ai_event_log_paging_widget import Ui_Widget

from widget.ai_event_log_page_button_frame_widget import AiEventLogPageButtonFrameWidget
from rpa.db.db_rpa_report import RpaReport  
from rpa.rpa_main_window import RpaMainWindow  

class LoadEventLogsQThread(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, current_page: int, page_size: int, start_dt: str, end_dt: str, selected_cctvs: dict, selected_events: list):
        super().__init__()
        self.setObjectName("LoadEventLogsQThread")
        self.page_size = page_size
        self.offset = (current_page - 1) * page_size
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.selected_cctvs = selected_cctvs
        self.selected_events = selected_events
    def run(self):
        try:
            event_logs = db_ai_event_log.get_ai_event_logs(start_dt=self.start_dt, end_dt=self.end_dt, selected_cctvs=self.selected_cctvs, selected_events=self.selected_events, limit=self.page_size, offset=self.offset)
            self.finished.emit(event_logs)
        except Exception as e:
            self.error.emit(str(e))

class CheckBoxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = index.data(Qt.CheckStateRole)
        check_box_style_option = QStyleOptionButton()
        check_box_style_option.state |= QStyle.State_Enabled

        if value == Qt.Checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)
        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)

    def editorEvent(self, event, model, option, index):
        return False    # 모든 이벤트 무시함 (Qt 기본동작도 무시함) : 체크박스 및 행 클릭 시 체크 상태 변경을 위해

    def getCheckBoxRect(self, option):
        # 중앙 정렬된 체크박스 영역 계산
        check_box_style_option = QStyleOptionButton()
        rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        x = option.rect.x() + (option.rect.width() - rect.width()) // 2
        y = option.rect.y() + (option.rect.height() - rect.height()) // 2
        return QRect(x, y, rect.width(), rect.height())
        
class AiEventLogPagingWidget(QWidget, Ui_Widget):
    table_cell_clicked = Signal(dict)
    ai_event_logs_loading_finished = Signal()

    def __init__(self, rap_dialog, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.rap_dialog = rap_dialog
        self.event_logs = []
        
        self.setup_ui()
        self.init_ui()


    def setup_ui(self):
        # 1열 (체크박스 열)은 고정 폭 30
        self.table_widget_ai_event_log.setColumnWidth(0, 20)
        self.table_widget_ai_event_log.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  # 고정 크기

        # 페이지 버튼 프레임
        self.ai_event_log_page_button_frame_widget = AiEventLogPageButtonFrameWidget()
        self.layout_page_button_frame.replaceWidget(self.label_ai_event_log_page_button_frame_widget, self.ai_event_log_page_button_frame_widget)
        self.label_ai_event_log_page_button_frame_widget.deleteLater()

    def init_ui(self):
        # 델리게이트 등록 (첫 번째 컬럼에 체크박스 델리게이트 적용)
        self.table_widget_ai_event_log.setItemDelegateForColumn(0, CheckBoxDelegate(self.table_widget_ai_event_log))
        
        # 기존 시그널 연결 해제 후 다시 연결 (중복 방지)
        try:
            self.table_widget_ai_event_log.cellClicked.disconnect(self.on_table_cell_clicked)
        except TypeError:
            # 연결된 시그널이 없는 경우 예외 발생, 무시
            pass
        self.table_widget_ai_event_log.cellClicked.connect(self.on_table_cell_clicked)

        # 검색 필터 값
        self.start_dt = QDateTime(QDate.currentDate(), QTime(0, 0, 0)).toString("yyyy-MM-dd HH:mm:ss")
        self.end_dt = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.selected_cctvs = {}
        self.selected_events = []

        # 페이징 처리
        self.current_page = 1
        self.max_visible_pages = 4
        self.page_size = 15

        self.update_page_buttons()
        self.load_event_logs()

    def update_page_buttons(self, should_change_page:bool = False):
        if not should_change_page:
            total_rows = db_ai_event_log.get_ai_event_logs(fields="COUNT('*')", start_dt=self.start_dt, end_dt=self.end_dt, selected_cctvs=self.selected_cctvs, selected_events=self.selected_events)[0]["COUNT('*')"]
            self.total_pages = (total_rows + self.page_size - 1) // self.page_size
            print(total_rows)
            self.label_total_event_logs.setText(f"총 {total_rows} 건")

        layout = self.ai_event_log_page_button_frame_widget.layout_page_button.layout()
        
        while layout.count():
            layout.takeAt(0).widget().deleteLater()

        # ◀ Prev
        button_prev_page = QPushButton("◀")
        button_prev_page.clicked.connect(self.on_button_prev_page_clicked)
        button_prev_page.setEnabled(self.current_page > 1)
        layout.addWidget(button_prev_page)

        # 페이지 번호 계산
        start = max(1, self.current_page - 1)
        end = min(start + self.max_visible_pages - 1, self.total_pages)
        if end - start < self.max_visible_pages - 1:
            start = max(1, end - self.max_visible_pages + 1)

        for page in range(start, end + 1):
            btn = QPushButton(str(page))
            btn.setCheckable(True)
            btn.setChecked(page == self.current_page)
            btn.clicked.connect(lambda _, p=page: self.change_page(p))
            layout.addWidget(btn)
        self.label_total_pages.setText(f"현재 페이지: {min(self.current_page, self.total_pages)}/{self.total_pages}")

        # ▶ Next
        button_next_page = QPushButton("▶")
        button_next_page.clicked.connect(self.on_button_next_page_clicked)
        button_next_page.setEnabled(self.current_page < self.total_pages)
        layout.addWidget(button_next_page)

    def change_page(self, page):
        self.current_page = page
        self.update_page_buttons(should_change_page=True)
        self.load_event_logs()

    def load_event_logs(self):
        self.load_thread = LoadEventLogsQThread(self.current_page, self.page_size, self.start_dt, self.end_dt, self.selected_cctvs, self.selected_events)
        self.load_thread.finished.connect(self.on_load_event_logs_finished)
        self.load_thread.error.connect(lambda msg: QMessageBox.critical(self, "이벤트 로그 불러오기 실패", msg))
        self.load_thread.start()

    def on_load_event_logs_finished(self, event_logs):
        table_widget = self.table_widget_ai_event_log
        table_widget.setUpdatesEnabled(False)
        table_widget.clearContents()
        table_widget.setRowCount(len(event_logs))

        self.event_logs = event_logs
        
        # 데이터 채우기
        for row, log in enumerate(event_logs):
            item_check = QTableWidgetItem()
            item_check.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
            item_check.setCheckState(Qt.Unchecked)
            item_check.setData(Qt.UserRole, log['image'])

            table_widget.setItem(row, 0, item_check)
            table_widget.setItem(row, 1, QTableWidgetItem(log['date'].strftime('%Y-%m-%d %H:%M:%S')))
            table_widget.setItem(row, 2, QTableWidgetItem(log['cctv_location']))
            table_widget.setItem(row, 3, QTableWidgetItem(log['cctv_id']))
            table_widget.setItem(row, 4, QTableWidgetItem(log['content']))
            table_widget.setItem(row, 5, QTableWidgetItem(log['severity']))
        
        table_widget.setUpdatesEnabled(True)

        self.ai_event_logs_loading_finished.emit()

    def display_search_results(self, start_dt: str, end_dt: str, selected_cctvs: dict, selected_events: list):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.selected_cctvs = selected_cctvs
        self.selected_events = selected_events

        self.update_page_buttons()
        self.load_event_logs()

    def create_report(self):
        table_widget = self.table_widget_ai_event_log

        selected_index = []
        for row in range(table_widget.rowCount()):
            check_state = table_widget.model().data(table_widget.model().index(row, 0), Qt.CheckStateRole)
            if check_state and check_state == Qt.Checked:
                selected_index.append(row)
            
        if not selected_index:
            QMessageBox.information(self, "보고서 작성", "선택된 이벤트가 없습니다.")
            return

        complete = []
        fail = []

        for row in selected_index:
            # if table_widget.item(row, 5) is None:
            #     return
                
            image_path = table_widget.item(row, 0).data(Qt.UserRole)
            event_time = table_widget.item(row, 1).text()
            location = table_widget.item(row, 2).text()
            CCTV = table_widget.item(row, 3).text()
            event_type = table_widget.item(row, 4).text()

            report = RpaReport()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report.event_time = event_time
            report.report_time = now
            report.title = f"{event_time}_이벤트 발생" 
            report.location = f'{location} {CCTV}'
            report.event_type = event_type
            report.severity = self.event_logs[row].get('severity', '')
            report.image_path = image_path
            val = report.insert()

            if val and 0 <= val:
                complete.append(row)
            else:
                fail.append(row)
                
        if 0 < len(fail):
            QMessageBox.critical(self, "보고서 작성", "보고서 작성 실패")
        else:
            QMessageBox.information(self, "보고서 작성", "보고서 작성 완료")

        # 보고서 위젯 표시
        if self.rap_dialog is None:
            self.rap_dialog = RpaMainWindow()

        self.rap_dialog.show()

    def on_button_prev_page_clicked(self):
        if self.current_page > 1:
            self.change_page(self.current_page-1)

    def on_button_next_page_clicked(self):
        if self.current_page < self.total_pages:
            self.change_page(self.current_page+1)

    def on_table_cell_clicked(self, row, column):
        table_widget = self.table_widget_ai_event_log

        index = table_widget.model().index(row, 0)
        current_state = table_widget.model().data(index, Qt.CheckStateRole)
        new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
        table_widget.model().setData(index, new_state, Qt.CheckStateRole)

        header_labels = ['checked', 'date', 'cctv_location', 'cctv_id', 'content','severity']
        # 해당 행의 모든 열 값을 딕셔너리에 담기
        row_data = {}
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            if col == 0:
                # 체크박스 값은 체크 상태(bool)로 저장
                check_state = Qt.Checked if table_widget.model().data(table_widget.model().index(row, col), Qt.CheckStateRole) == Qt.Checked else Qt.Unchecked
                row_data[header_labels[col]] = (check_state == Qt.Checked)
                row_data['image'] = item.data(Qt.UserRole)
            else:
                row_data[header_labels[col]] = item.text() if item else ''
        self.table_cell_clicked.emit(row_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogPagingWidget(None)
    widget.show()  
    sys.exit(app.exec()) 