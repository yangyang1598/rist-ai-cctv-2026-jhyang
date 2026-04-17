import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db.db_cctv_list as db_cctv_list

from PySide6.QtWidgets import QWidget, QApplication, QTableWidgetItem
from PySide6.QtCore import QSize, Qt, QTimer

from widget.video_process_pipeline.video_process_manager import ProcessManager
from ui.ui_cctv_connection_status_widget import Ui_Widget
from setting import paths
from setting.use_qsetting import Setting

from rich.console import Console
console = Console()

"""
TODO: 2025-09-02 시스템 상태 - CCTV 프로세스 Health Check 기능 수정

self.process_manager.processes = {
    0: <Process name='VideoProcess-0' pid=330904 parent=330815 started daemon>,
    1: <Process name='VideoProcess-1' pid=330905 parent=330815 started daemon>,
    ...
    20: <Process name='VideoProcess-20' pid=330980 parent=330815 stopped exitcode=0 daemon>,
    21: <Process name='VideoProcess-21' pid=330981 parent=330815 stopped exitcode=0 daemon>,
    22: <Process name='VideoProcess-22' pid=330982 parent=330815 stopped exitcode=0 daemon>,
    23: <Process name='VideoProcess-23' pid=330983 parent=330815 stopped exitcode=0 daemon>,
    24: <Process name='VideoProcess-24' pid=330984 parent=330815 stopped exitcode=0 daemon>
}
self.process_manager.active_camera_list = {
    0: {'camera_id': 1, 'camera_location': '1공장', 'camera_name': 'CCTV 1'},
    1: {'camera_id': 2, 'camera_location': '1공장', 'camera_name': 'CCTV 2'},
    2: {'camera_id': 3, 'camera_location': '1공장', 'camera_name': 'CCTV 3'},
    3: {'camera_id': 4, 'camera_location': '1공장', 'camera_name': 'CCTV 4'},
    ...
}

for p in self.process_manager.processes.values():
    console.log(p.name, p.pid, p.is_alive(), p.exitcode)

p.name          p.pid    p.is_alive()   p.exitcode
VideoProcess-19 333916   True           None
VideoProcess-24 333971   False          0

Background Process가 RTSP 수신 실패 등의 이유로 exit되었을 때 p.is_alive()인지 or p.exitcode가 None이 아닌지 여부를 체크해야 함

"""

SETTING_DICT: dict =  Setting(paths.GLOBAL_SETTING_PATH).to_dict()
GLOBAL_SETTING: dict = SETTING_DICT.get("global", {})
SYSTEM_CHECK_TIME: int = int(GLOBAL_SETTING.get("system_check_time", 5)) # 시스템 상태 점검 주기 (초)

class CctvConnectionStatusWidget(QWidget, Ui_Widget):
    def __init__(self, process_manager):
        super().__init__()
        self.setupUi(self)
        # self.cctv_connection_status_dict = {"all": 75, "normal": 65, "abnormal": 10}  
        self.process_manager: ProcessManager = process_manager
        
        self.init_timer()

    def sizeHint(self):
        # 메인 윈도우에 붙일 때, 기본 크기를 너비 300, 높이 65으로 지정
        return QSize(300, 40)

    def init_timer(self):
        # UI 초기화 시 테이블 항목 채우기 (초기값)
        self.update_cctv_connection_table()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cctv_connection_table)
        self.timer.start(SYSTEM_CHECK_TIME * 1000)  # 1분마다

    def set_background_controller_process_manager(self, process_manager):
        self.process_manager = process_manager

    def update_cctv_connection_table(self):
        cctvs = db_cctv_list.get_cctv_list('camera_location, camera_name')
        cctv_count = len(cctvs)
        if self.process_manager:
            active_count = 0
            for video_id, process in self.process_manager.processes.items():
                # 1. 프로세스가 살아있는지
                is_alive = process.is_alive()
                # 2. 정상 종료되지 않았는지
                is_not_terminated = process.exitcode is None
                # 3. 스트림이 정상인지
                is_healthy = self.process_manager.is_stream_healthy(video_id)
                
                # 세 조건을 모두 만족해야 활성화로 간주
                if is_alive and is_not_terminated and is_healthy:
                    active_count += 1
                elif not is_healthy and is_alive:
                    # 프로세스는 살아있지만 스트림이 비정상인 경우 디버그 로그
                    camera_name = self.process_manager.active_camera_list.get(video_id, {}).get("camera_name", f"Video{video_id}")
                    # print(f"[DEBUG] {camera_name}: 프로세스 활성, 스트림 비정상")
            
            inactive_count = cctv_count - active_count

            print(f"[{time.strftime('%H:%M:%S', time.localtime())}] 전체 {cctv_count}개 중 {active_count}개가 활성화됨 - cctv_connection_status_widget.py:L49")
            values = [cctv_count, active_count, inactive_count]
        else:
            values = ["-"] * 3

        for col, val in enumerate(values):
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget_cctv_connection_status.setItem(0, col, item)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CctvConnectionStatusWidget()
    widget.show()  
    sys.exit(app.exec()) 
