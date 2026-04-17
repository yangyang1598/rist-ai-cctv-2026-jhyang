import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QDateTime, QDate, QTime, Signal, QTimer

from ui.ui_ai_event_log_filter_search_widget import Ui_Widget

class AiEventLogFilterSearchWidget(QWidget, Ui_Widget):
    search_requested = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_ui()
        self.init_ui()

    def setup_ui(self):
        self.layout_search.insertSpacing(2, 10)
        self.layout_search.insertSpacing(1, 5)
        self.layout_event_log_filter_search.insertSpacing(1, 5)

    def init_ui(self):
        self.set_datetime_range(QDateTime(QDate.currentDate(), QTime(0, 0, 0)), QDateTime.currentDateTime())

        self.button_search.clicked.connect(self.search_by_datetime)
        self.button_search_by_week.clicked.connect(lambda: self.search_by_quick_filter("week"))
        self.button_search_by_month.clicked.connect(lambda: self.search_by_quick_filter("month"))
        self.button_search_by_year.clicked.connect(lambda: self.search_by_quick_filter("year"))

    def set_search_buttons_enabled(self, enabled: bool):
        buttons = [
            self.button_search, self.button_search_by_week, 
            self.button_search_by_month, self.button_search_by_year
        ]

        for btn in buttons:
            btn.setEnabled(enabled)

    def set_datetime_range(self, start_dt, end_dt):
        self.datetime_start_date_filter.setDateTime(start_dt)
        self.datetime_end_date_filter.setDateTime(end_dt)

    def search_by_quick_filter(self, period: str):
        now = datetime.now()

        if period == "week":
            start = now - timedelta(days=7)
        elif period == "month":
            start = now - relativedelta(months=1)
        elif period == "year":
            start = now - relativedelta(years=1)
        else:
            start = now

        start = start.replace(hour=0, minute=0, second=0, microsecond=0)

        self.set_datetime_range(start, now)

        self.search_by_datetime()

    def search_by_datetime(self):
        self.set_search_buttons_enabled(False)
        self.search_requested.emit(self.datetime_start_date_filter.text(), self.datetime_end_date_filter.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogFilterSearchWidget()
    widget.show()  
    sys.exit(app.exec()) 