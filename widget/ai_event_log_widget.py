import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import queue
import time

import db.db_ai_event_log as db_ai_event_log

from datetime import datetime

from PySide6.QtWidgets import QWidget, QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
from PySide6.QtCore import QObject, QThread, Signal

from ui.ui_ai_event_log_widget import Ui_Widget
from dialog.ai_event_log_image_popup_dialog import AiEventLogImagePopupDialog

class AddEventLogsQThread(QThread):
    finished = Signal(object)
    error = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("AddEventLogsQThread")
        self._running = True
        self._event_queue = queue.Queue()
        self._processing = False

    def stop(self):
        self._running = False

    def add_event_log(self, event_log):
        self._event_queue.put(event_log)

    def run(self):
        while self._running:
            if not self._event_queue.empty() and not self._processing:
                self._processing = True
                event_log = self._event_queue.get()
                try:
                    date = datetime.fromtimestamp(event_log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    event_logs = db_ai_event_log.insert_ai_event_log(
                        date=date, cctv_location=event_log.cctv_location, 
                        cctv_name=event_log.cctv_name, event=event_log.event_name, severity=event_log.severity,image_path=event_log.image_path,
                        )
                    # print(f"!!!!!!!!!!!!!!!!!!!insert result : {event_logs}!!!!!!!!!!!!!!!!!!!!!!!")
                    self.finished.emit(event_log)
                except Exception as e:
                    self.error.emit(str(e))
                finally:
                    self._processing = False
            else:
                self.msleep(10)  # busy waiting 방지

class AiEventLogWidget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.add_event_log_thread = AddEventLogsQThread()
        self.add_event_log_thread.finished.connect(self.on_add_event_log_finished)
        self.add_event_log_thread.error.connect(lambda msg: QMessageBox.critical(self, "이벤트 로그 저장 실패", msg))
        self.add_event_log_thread.start()


        
        self.table_widget_ai_event_log.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_ai_event_log.cellDoubleClicked.connect(self.handle_row_click)

        self.load_event_logs_to_table(self.table_widget_ai_event_log)

    def load_event_logs_to_table(self, table_widget:QTableWidget):
        event_logs = db_ai_event_log.get_ai_event_logs(limit=100)
        table_widget.setRowCount(len(event_logs))
        for row, log in enumerate(event_logs):
            
            date_obj = datetime.fromisoformat(str(log['date']))
            table_widget.setItem(row, 0, QTableWidgetItem(date_obj.strftime('%Y-%m-%d %H:%M:%S')))
            table_widget.setItem(row, 1, QTableWidgetItem(log['cctv_location']))
            table_widget.setItem(row, 2, QTableWidgetItem(log['cctv_id']))
            table_widget.setItem(row, 3, QTableWidgetItem(log['content']))
            table_widget.setItem(row, 4, QTableWidgetItem(log['severity']))
            table_widget.setItem(row, 5, QTableWidgetItem(log['image']))

    def handle_row_click(self, row, column):
        last_col = self.table_widget_ai_event_log.columnCount() - 1
        item = self.table_widget_ai_event_log.item(row, last_col)
        if item:
            image_path = item.text()
            popup = AiEventLogImagePopupDialog(image_path)
            popup.exec()

    def add_event_log_to_table(self, event_log):
        self.add_event_log_thread.add_event_log(event_log)

    def on_add_event_log_finished(self, event_log):
        table_widget = self.table_widget_ai_event_log

        # 현재 행 수가 max_rows 이상이면 마지막 행 제거
        if table_widget.rowCount() >= 100:
            table_widget.removeRow(table_widget.rowCount() - 1)

        # 맨 위에 새 행 삽입
        table_widget.insertRow(0)

        date = datetime.fromtimestamp(event_log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        row_data = [date, event_log.cctv_location, event_log.cctv_name, event_log.event_name, event_log.severity, event_log.image_path]

        for col, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            table_widget.setItem(0, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogWidget()
    widget.show()  
    sys.exit(app.exec()) 
