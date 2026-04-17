import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.ui_system_status_dialog import Ui_Dialog

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Qt, QTimer

from widget.status_widget import StatusWidget
from widget.resource_monitor_widget import ResourceMonitorWidget
from setting import paths
from setting.use_qsetting import Setting


SETTING_DICT: dict =  Setting(paths.GLOBAL_SETTING_PATH).to_dict()
GLOBAL_SETTING: dict = SETTING_DICT.get("global", {})
SYSTEM_CHECK_TIME: int = int(GLOBAL_SETTING.get("system_check_time", 5)) # 시스템 상태 점검 주기 (초)

class SystemStatusDialog(QDialog, Ui_Dialog):
    def __init__(self, process_manager):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("시스템 상태 확인")

        self.process_manager = process_manager

        self.setup_ui()
        self.init_timer()

    def setup_ui(self):
        self.tab_widget_system_status.setCurrentIndex(0)

        # CCTV 연결 상태
        self.cctv_status_widget = StatusWidget(self.process_manager, 'cctv')
        self.layout_cctv_status.replaceWidget(self.label_cctv_status_widget, self.cctv_status_widget)
        self.label_cctv_status_widget.deleteLater()

        # 이벤트 감지 상태
        self.event_status_widget = StatusWidget(self.process_manager, 'event')
        self.layout_event_status.replaceWidget(self.label_event_status_widget, self.event_status_widget)
        self.label_event_status_widget.deleteLater()

        # 서버 상태
        self.server_status_widget = ResourceMonitorWidget()
        self.layout_server_status.replaceWidget(self.label_server_status_widget, self.server_status_widget)
        self.label_server_status_widget.deleteLater()


    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cctv_status)
        self.timer.start(SYSTEM_CHECK_TIME * 1000)  # 1분마다

    def update_cctv_status(self):
        self.cctv_status_widget.update_cctv_status()
        self.event_status_widget.update_cctv_status()

    def update_event_status(self, event_log):
        self.event_status_widget.update_event_status(event_log)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SystemStatusDialog(None)
    widget.show()
    sys.exit(app.exec())