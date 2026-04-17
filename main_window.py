import os, sys, json, time, multiprocessing as mp, shutil, re
from memory_profiler import profile
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QPixmap, QIcon, QImage,QAction
from PySide6.QtSvgWidgets import QSvgWidget

from ui.ui_main_window import Ui_MainWindow
from setting.use_qsetting import Setting

from widget.clock_widget import ClockWidget
from widget.cctv_connection_status_widget import CctvConnectionStatusWidget
from widget.cctv_list_widget import CctvListWidget
from widget.video_layout_widget import VideoLayoutWidget
from widget.ptz_controller_widget import PtzControllerWidget
from widget.ai_event_log_widget import AiEventLogWidget
from widget.ai_event_log_image_widget import AiEventLogImageWidget
from widget.video_process_pipeline.video_player_widget import VideoPlayerWidget
from widget.video_process_pipeline.video_display_widget import VideoDisplayWidget
from widget.video_process_pipeline.video_config import VideoConfig, LayoutData, setup_logger, MessageType, EventLogData
from widget.video_process_pipeline.background_controller import BackgroundController
from widget.model_management_widget import TemperaryLayout
from widget.snapshot_image_widget import TabSnapshotImageWidget



from dialog.system_status_dialog import SystemStatusDialog
from dialog.ai_event_log_search_dialog import AiEventLogSearchDialog
from dialog.cctv_setting_dialog import CctvSettingDialog
from dialog.management_dialog import ManagementDialog
from dialog.auto_delete_setting_dialog import AutoDeleteSettingDialog
from rpa.rpa_main_window import RpaMainWindow  

TARGET_PATH: str = "/home/skysys/rist-ai-cctv-2025-2nd" #skysys용
# TARGET_PATH: str = "/home/rist/rist-ai-cctv-2025-2nd" # Posco용
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.logger = setup_logger("MainWindow")
        self.setting = Setting("global_setting.ini")
        self.setupUi(self)
        self.setup_ui()
        self.init_ui()
        
        self._check_and_free_space_running = False
        self._perform_file_deletion_running = False  # 파일 삭제 함수 실행 상태
        self._disk_warning_dialog = None  # 팝업창 인스턴스 저장용
        self.button_delete_selected_layout.setVisible(False)
        
    def setup_ui(self):
        self.setWindowTitle("지능형 CCTV 플랫폼")
        self.setWindowIcon(QIcon("src/icon/main_icon.ico"))  # 아이콘 파일 경로 설정

        self.layout_left.insertSpacing(2, 10)
        self.layout_left.insertSpacing(1, 10)

        # 로고
        pixmap = QPixmap(self.load_file("src/icon", "POSCO.png"))
        self.label_logo.setPixmap(pixmap)

        # 현재 시간
        self.layout_left.replaceWidget(self.label_clock_widget, ClockWidget())
        self.label_clock_widget.deleteLater()

        # CCTV 연결 상태
        self.cctv_connection_status_widget = CctvConnectionStatusWidget(None)
        self.layout_left.replaceWidget(self.label_cctv_connection_status_widget, self.cctv_connection_status_widget)
        self.label_cctv_connection_status_widget.deleteLater()

        # CCTV 목록
        self.cctv_list_widget = CctvListWidget()
        self.layout_left.replaceWidget(self.label_cctv_list_widget, self.cctv_list_widget)
        self.label_cctv_list_widget.deleteLater()

        # 레이아웃 구성 목록
        self.tab_count: int = 1
        self.tab_data: dict = {}
        self.video_player_widget_list: list[VideoPlayerWidget] = []
        self.video_config = VideoConfig()
        self.set_live_tab_widget(f"Live")

        self.current_video_layout_name: str = ""
        self.video_layout_widget = VideoLayoutWidget(self.video_player_widget_list[0])
        self.layout_left.replaceWidget(self.label_video_layout_widget, self.video_layout_widget)
        self.label_video_layout_widget.deleteLater()

        # PTZ 제어
        self.ptz_controller_widget = PtzControllerWidget()
        self.layout_left.replaceWidget(self.label_ptz_controller_widget, self.ptz_controller_widget)
        self.label_ptz_controller_widget.deleteLater()

        # 이벤트 로그
        self.ai_event_log_widget = AiEventLogWidget()
        self.layout_center.replaceWidget(self.label_ai_event_log_widget, self.ai_event_log_widget)
        self.label_ai_event_log_widget.deleteLater()

        # 이벤트 로그 이미지 사이드바(오른쪽)
        self.ai_event_log_image_widget = AiEventLogImageWidget()
        self.layout_right.replaceWidget(self.label_event_log_image_widget, self.ai_event_log_image_widget)
        self.label_event_log_image_widget.deleteLater()

        self.rap_dialog = RpaMainWindow()
        self.rap_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.temperary_layout=TemperaryLayout()
        
        self.ai_event_log_search_dialog = AiEventLogSearchDialog(self.rap_dialog)
        self.cctv_setting_dialog = CctvSettingDialog()
        self.auto_delete_dialog=AutoDeleteSettingDialog()     

        # 스냅샷 이미지
        self.snapshot_image_widget = TabSnapshotImageWidget()
        self.gridLayout.replaceWidget(self.label_snapshot_image_widget, self.snapshot_image_widget)
        self.label_snapshot_image_widget.deleteLater()

        # 사이드바 감추기
        # self.hide_side_bar()
        # self.hide_event_log()
        # self.ai_event_log_image_widget.hide()

    def init_ui(self):
        # CCTV 목록
        self.cctv_list_widget.stream_info_selected.connect(self.on_cctv_list_stream_info_selected)
        
        #탭 추가/삭제 버튼 숨김
        self.button_add_tab.hide()
        self.button_remove_tab.hide()
        # 비디오 디스플레이 탭 추가/삭제
        # self.button_add_tab.clicked.connect(self.on_button_add_tab_clicked)
        # self.button_remove_tab.clicked.connect(self.on_button_remove_tab_clicked)
        self.tab_widget_video_player.currentChanged.connect(self.on_tab_changed)

        # 비디오 디스플레이 레이아웃
        self.button_video_player_layout_1x1.clicked.connect(lambda: self.create_current_tab_grid(1))
        self.button_video_player_layout_2x2.clicked.connect(lambda: self.create_current_tab_grid(2))
        self.button_video_player_layout_3x3.clicked.connect(lambda: self.create_current_tab_grid(3))
        self.button_video_player_layout_4x4.clicked.connect(lambda: self.create_current_tab_grid(4))
        self.button_video_player_layout_5x5.clicked.connect(lambda: self.create_current_tab_grid(5))

        # 레이아웃 구성 목록
        self.video_layout_widget.grid_data.connect(self.get_layout_data_and_play_all_cctv_stream_in_layout_data)

        # 이벤트 로그 이미지 목록 토글
        self.button_ai_event_image_log.clicked.connect(self.toggle_event_log_image_widget)

        # 프로그램
        self.action_system_status.triggered.connect(self.open_system_status_dialog)
        self.action_event_logs.triggered.connect(self.open_ai_event_log_search_dialog)

        # 설정
        self.action_cctv_settings.triggered.connect(self.open_cctv_setting_dialog)  # CCTV 설정 대화상자 열기
        self.action_rpa_settings.triggered.connect(self.open_cctv_rpa_settings)
        self.action_auto_delete_settings.triggered.connect(self.open_auto_delete_settings_dialog)
        
        # 관리자 메뉴
        self.action_event_logic_management.triggered.connect(self.open_event_logic_management_dialog)
        self.action_ai_train_management.triggered.connect(self.open_model_list_management_dialog)  # AI 트레이닝 관리 대화상자 열기
        self.action_cctv_management.triggered.connect(self.open_cctv_management_dialog)  # CCTV 관리 대화상자 열기

        #모델 파일 변환
        self.temperary_layout.save_layout.connect(self.set_temper_layout)
        self.temperary_layout.clear_ui.connect(self.clear_temper_ui)
        self.temperary_layout.load_layout.connect(self.load_temper_layout)
        self.temperary_layout.delete_layout.connect(self.del_temper_layout)

        # 그리드 수정 모드 or PTZ 모드 
        self.is_layout_modify: bool = False
        self.button_modify_layout.toggled.connect(self.change_layout_modify_button_text)

        # 레이아웃 구성 삭제
        self.button_delete_selected_layout.clicked.connect(self.delete_selected_layout)

        # 사이드바 활성화 & 버튼 텍스트 변경(20250908 기본 UI 내 사이드바 x 구현)
        self.button_show_sidebar.toggled.connect(self.change_side_bar_button_text)
        self.button_show_event_log.toggled.connect(self.change_event_log_button_text)

        # TODO: 2025-10-15
        # 메뉴바에 스트림 재시작 메뉴 추가
        # video_process에서 스트림 재연결 최대 횟수 초과 시 스트림 재시작 수동 기능
        # 현재 미구현 <- 지금은 재연결 횟수를 사실상 무한으로 설정하였음

        # 메뉴바의 스트림 재시작 메뉴 -> 액션 형식으로 변경
        # self.menubar.removeAction(self.menu_restart_stream.menuAction())
        # self.action_restart_stream = QAction("스트림 재시작", self)
        # self.action_restart_stream.triggered.connect(self.restart_stream)
        # self.menubar.addAction(self.action_restart_stream)

    def restart_stream(self):
        print("!!!!!!!!!!!!clicked restart_stream!!!!!!!!")

    def load_file(self, *path_parts):
        return os.path.join(os.path.dirname(__file__), *path_parts)

    def change_side_bar_button_text(self, checked: bool):
        
        if not checked:
            self.button_show_sidebar.setText(">")
            self.show_side_bar()
        else:
            self.button_show_sidebar.setText("<")
            self.hide_side_bar()
    
    def change_event_log_button_text(self,checked:bool):
        if not checked:
            self.button_show_event_log.setText("v")
            self.show_event_log()    
        else:
            self.button_show_event_log.setText("^")
            self.hide_event_log()
            
    def hide_event_log(self):
        self.ai_event_log_widget.hide()

    def hide_side_bar(self):
        # 왼쪽 사이드바 감춤
        for i in range(self.layout_left.count()):
            item = self.layout_left.itemAt(i)
            if item:
                if item.widget():
                    item.widget().hide()
                elif item.layout():
                    # 로그인 정보 위젯들을 재귀적으로 숨김
                    self._set_label_id_visible(item.layout(), False)
        
        self.hide_layout_buttons()

    def hide_layout_buttons(self):
        """레이아웃 관련 버튼들을 숨기기"""
        # 비디오 레이아웃 버튼들
        self.button_video_player_layout_1x1.setVisible(False)
        self.button_video_player_layout_2x2.setVisible(False)
        self.button_video_player_layout_3x3.setVisible(False)
        self.button_video_player_layout_4x4.setVisible(False)
        self.button_video_player_layout_5x5.setVisible(False)
        
        # 탭 관련 버튼들
        self.button_add_tab.setVisible(False)
        self.button_remove_tab.setVisible(False)

        # 레이아웃 버튼
        self.button_modify_layout.setVisible(False)

    def show_event_log(self):
        self.ai_event_log_widget.show()

    def show_side_bar(self):
        # 왼쪽 사이드바 표시
        for i in range(self.layout_left.count()):
            item = self.layout_left.itemAt(i)
            if item:
                if item.widget():
                    item.widget().show()
                elif item.layout():
                    # 로그인 정보 위젯들을 재귀적으로 표시
                    self._set_label_id_visible(item.layout(), True)
        
        self.show_layout_buttons()

    def _set_label_id_visible(self, layout, visible):
        """로그인 정보 위젯 가시성 설정"""
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().setVisible(visible)
            elif item.layout():
                self._set_label_id_visible(item.layout(), visible)
   
    def show_layout_buttons(self):
        """레이아웃 관련 버튼들을 보이기"""
        # 비디오 레이아웃 버튼들
        self.button_video_player_layout_1x1.setVisible(True)
        self.button_video_player_layout_2x2.setVisible(True)
        self.button_video_player_layout_3x3.setVisible(True)
        self.button_video_player_layout_4x4.setVisible(True)
        self.button_video_player_layout_5x5.setVisible(True)
        
        # 탭 관련 버튼들
        self.button_add_tab.setVisible(True)
        self.button_remove_tab.setVisible(True)

        # 레이아웃 버튼
        self.button_modify_layout.setVisible(True)

    @Slot(str)
    def set_temper_layout(self,text:str):
        print(f"set_temper_layout: {text}")
        self.video_layout_widget.add_model_video_layout(text)

    @Slot()
    def clear_temper_ui(self):
        """임시 레이아웃 위젯 초기화"""
        self.video_player_widget_list[0].clear_grid_widget()

    @Slot(str)
    def load_temper_layout(self, text:str):
        self.video_layout_widget.find_layout_by_name(text)
        
    @Slot(str)
    def del_temper_layout(self, text:str):
        self.video_layout_widget.delete_model_video_layout(text)
        
    #region 탭 및 비디오 플레이어 위젯 생성 관련 함수
    def set_live_tab_widget(self, tab_name):
        """비디오 플레이어 위젯 공통 생성 로직"""
        video_player_widget = VideoPlayerWidget(self.tab_count, main_window=self)
        self.tab_widget_video_player.insertTab(0, video_player_widget, tab_name)
        self.tab_widget_video_player.setCurrentIndex(0)

        # 시그널 연결
        video_player_widget.clicked_cctv_info.connect(self.video_control)

        self.video_player_widget_list.append(video_player_widget)
        self.logger.info(f"{video_player_widget.player_widget_index} 인스턴스 생성됨: 탭 {self.tab_count}")
        # self.tab_count += 1

    def create_current_tab_grid(self, grid_size: int):
        """현재 활성화된 탭의 비디오 플레이어 위젯에만 그리드를 생성"""
        self.current_video_layout_name = ""
        current_tab_index = self.tab_widget_video_player.currentIndex()
        if current_tab_index >= 0 and current_tab_index < len(self.video_player_widget_list):
            current_video_player_widget = self.video_player_widget_list[current_tab_index]
            current_video_player_widget.create_grid(grid_size)
        
    # def on_button_add_tab_clicked(self):
    #     self.set_live_tab_widget(f"탭 {self.tab_count}")

    # def on_button_remove_tab_clicked(self):
    #     index = self.tab_widget_video_player.currentIndex()
    #     tab_name = self.tab_widget_video_player.tabText(index)
    #     if index != -1:
    #         self.tab_widget_video_player.removeTab(index)

    #     current_tab_index = self.tab_widget_video_player.currentIndex()
    #     if current_tab_index >= 0 and current_tab_index < len(self.video_player_widget_list):
    #         current_video_player_widget = self.video_player_widget_list[current_tab_index]
    #         current_video_player_widget.is_grid_creating = False
    #         current_video_player_widget.clear_grid_widget()
    #     self.tab_count -= 1
    #     self.logger.info(f"{tab_name} 삭제됨")

    def change_layout_modify_button_text(self, checked: bool):
        """
        레이아웃 수정 완료 버튼 눌렀을 때 현재 레이아웃 설정 수정 기능
        """
        video_player_widget: VideoPlayerWidget = self.video_player_widget_list[0]

        if not checked:
            self.button_modify_layout.setText("레이아웃 수정")
            self.is_layout_modify = False
            video_player_widget.set_layout_modify_mode(False)
            self.button_delete_selected_layout.setVisible(False)
            if self.current_video_layout_name:
                new_video_data = self.video_layout_widget.find_grid_layout()
                self.video_layout_widget.update_video_layout(self.current_video_layout_name, new_video_data)
        else:
            self.button_modify_layout.setText("수정 완료")
            self.is_layout_modify = True
            video_player_widget.set_layout_modify_mode(True)
            self.button_delete_selected_layout.setVisible(True)

    def delete_selected_layout(self):
        """
        레이아웃 삭제 버튼 클릭 시 현재 레이아웃 설정 삭제

        {'camera_id': 1, 'camera_ip': 'localhost', 'camera_name': 'CCTV 1', 'port': 8554, 'ptz_port': 0, 'rtsp_id': '', 'rtsp_pw': '', 'video_num': 0}
        """
        if self.clicked_cctv_info:
            video_num = self.clicked_cctv_info.get("video_num", -1)
            video_player_widget = self.video_player_widget_list[0]
            video_player_widget._clear_outline(video_num)
            video_player_widget.remove_video_widget(video_num)
            video_player_widget.first_selected_index_for_swap = -1
            video_player_widget.selected_grid_index = -1

    def on_tab_changed(self, index):
        """
        탭이 변경될 때 호출되는 슬롯 함수
        현재 탭의 인덱스를 출력합니다.
        """
        tab_text = self.tab_widget_video_player.tabText(index)
        is_live = tab_text != "Snapshot"

        # "Snapshot" 탭이면 비활성화, 그 외(Live 등)는 활성화
        self.check_activate_grid.setEnabled(is_live)
        self.button_video_player_layout_1x1.setEnabled(is_live)
        self.button_video_player_layout_2x2.setEnabled(is_live)
        self.button_video_player_layout_3x3.setEnabled(is_live)
        self.button_video_player_layout_4x4.setEnabled(is_live)
        self.button_video_player_layout_5x5.setEnabled(is_live)
        self.button_modify_layout.setEnabled(is_live)

    #endregion

    #region CCTV 관련 함수
    @Slot(dict)
    def on_cctv_list_stream_info_selected(self, cctv_info: dict):
        """
        비디오 플레이어 재생 함수
        선택된 CCTV 정보를 받아 비디오를 재생합니다.

        Parameters
        ----------
        - cctv_info : dict
            다음 키를 포함하는 CCTV 정보 딕셔너리:
            - stream_info
                - camera_ip : str
                    CCTV 카메라의 IP 주소 (예: "192.168.88.174").
                - camera_location : str
                    CCTV의 물리적 위치 (예: "1공장").
                - camera_name : str
                    CCTV의 이름 (예: "CCTV 1").
                - id : int
                    CCTV의 고유 식별자 (예: 12).
                - port : int
                    스트림에 사용되는 포트 번호 (예: 8554).
                - protocol : str
                    스트리밍에 사용되는 프로토콜 (예: "TCP").
                - rtsp_id : str
                    RTSP 인증 ID (비어 있을 수 있음).
                - rtsp_pw : str
                    RTSP 인증 비밀번호 (비어 있을 수 있음).
                - stream_url : str
                    스트림의 전체 RTSP URL (예: "rtsp://192.168.88.174:8554/test1").
            - events : list[dict]
                위험상황 이벤트 정보.
                    - name : str
                        위험상황 이벤트 이름.(예: "사람감지").
                    - skip_frame : int
                        건너뛸 프레임 수 (예: 1).
                    - input_img_size: int
                        이미지 사이즈 (예: 640)
                    - risk_level: int
                        이벤트 감지 시 알림 레벨 (0: 위험, 1: 주의)
                    - model_names : list[str]
                    - models: list[dict]
                        이벤트 내 모델 및 알고리즘 정보
                        - type: str
                            AI 인지 알고리즘인지 확인
                        - class_index: int
                            비디오 플레이어 내 표시 및 감지 시 알림 보낼 객체의 인덱스 
                        - class_name: str
                            비디오 플레이어 내 표시 및 감지 시 알림 보낼 객체의 이름
                        - name: str
                            type이 AI인 경우 트리톤 서버 내 업로드 이름 (예: "yolov8, yolov8_1")
                            type이 Algorithm인 경우 알고리즘 이름 (예: 거리, 무게 등)
        """
        self.video_config.is_visualize = cctv_info["is_visualize"]
        self.video_config.event = cctv_info["events"]
        self.video_config.camera_info = cctv_info["stream_info"]

        current_tab_index = self.tab_widget_video_player.currentIndex()
        self.play_video(current_tab_index)

    def play_video(self, current_tab_index: int):
        """CCTV 선택 시 (on_cctv_list_stream_info_selected) -> 현재 탭의 비디오 플레이어 위젯에서 비디오를 재생하는 함수"""
        camera_info: dict = self.video_config.camera_info
        camera_id = camera_info.get('id', -1)
        camera_name = camera_info.get('camera_name', 'Unknown')
        video_player_widget = self.video_player_widget_list[current_tab_index]
        background_video_list = self.background_controller.get_video_list()
        
        video_config = None
        for config in background_video_list:
            if config.camera_info["id"] == camera_id:
                video_config = config
                break

        # 백그라운드 컨트롤러에서 비디오가 이미 재생 중인지 확인 후 비디오 플레이어 위젯에 추가
        if video_config:
            # 기존 비디오 플레이어에서 레이아웃 데이터를 불러와서 중복 실행하는지 확인 <- 현재 백그라운드 영상에서 같은 CCTV를 동시에 1개만 재생 가능 (한 탭에서 여러개, 혹은 여러 탭에서 재생 불가능)
            layout_data = video_player_widget.get_current_layout_data()
            if layout_data and layout_data.cctv_info:
                for config in layout_data.cctv_info.values():
                    if config.camera_info.get('id') == camera_id:
                        QMessageBox.information(self, "재생 중", f"{camera_name} 은/는 이미 재생 중입니다.")
                        return
                    
            is_exist_background = True
            video_player_widget.play(video_config, is_exist_background)
            QTimer.singleShot(1000, lambda: self.activate_visualization(video_config))

            self.logger.info(f"{camera_name} (ID: {camera_id})의 기존 백그라운드 프로세스를 재사용합니다.")
        else:
            # 백그라운드 컨트롤러에서 비디오가 재생 중이지 않은 경우 새 영상 프로세스 생성
            is_exist_background = False
            video_player_widget.play(self.video_config, is_exist_background)
            video_player_widget.frame_receiver.event_log_received.connect(self.on_event_log_received)

    def activate_visualization(self, video_config):
        """UI 위젯 생성 완료 후 시각화 활성화"""
        self.background_controller.process_manager.send_command(
            video_config.video_number,
            {'type': MessageType.UPDATE_VISUALIZATION, 'is_visualize': True}
        )

    def play_all_cctv_streams(self, max_num: int = -1):
        """프로그램 초기 실행 시 DB에서 모든 CCTV 정보를 읽고 순차재생"""
        cctv_list = self.cctv_list_widget.get_all_items_info()
        self.background_controller = BackgroundController(cctv_list, max_num, self.video_player_widget_list)
        self.background_controller.frame_receiver.event_log_received.connect(self.on_event_log_received)
        self.background_controller.frame_receiver.event_status_received.connect(self.on_event_status_changed)
        self.background_controller.metrics_updated.connect(self.on_metrics_updated)

        self.cctv_connection_status_widget.set_background_controller_process_manager(self.background_controller.process_manager)
        self.management_dialog = ManagementDialog(self.temperary_layout,self.background_controller)
        # self.background_controller.frame_receiver.frame_received.connect(self.on_background_frame_received)
        self.system_status_dialog = SystemStatusDialog(self.background_controller.process_manager)
        self.system_status_dialog.hide()
        
    def _check_and_free_space(self, root_dir=TARGET_PATH):
        """
        디스크 공간을 확인하고 필요시 파일을 삭제하는 함수
        """
        # 이미 실행 중인 경우 삭제 작업만 수행
        if self._check_and_free_space_running:
            print("_check_and_free_space가 이미 실행 중입니다. 삭제 작업만 진행합니다.")
            self._perform_file_deletion(root_dir)
            return
        
        try:
            # 함수 실행 상태 설정
            self._check_and_free_space_running = True
            
            try:
                # 설정 파일을 다시 읽어서 최신 값 가져오기
                if os.path.exists(self.setting.settings_file):
                    self.setting.config.read(self.setting.settings_file, encoding='utf-8')
                
                # setting에서 값 가져오기
                required_capacity_mb = int(self.setting.get("required_capacity", "100", group="자동 정리 설정"))
                
            
            except (ValueError, TypeError) as e:
                self.logger.error(f"설정값 읽기 오류: {e}. 기본값 사용.")
                required_capacity_mb = 100
            
            
            # 디스크 사용량 확인
            total, used, free = shutil.disk_usage(root_dir)
            free_space_mb = free / (1024 * 1024)
            
            # 공간이 충분한 경우 함수 종료
            if free_space_mb >= required_capacity_mb:
                # self.logger.info(f"디스크 공간이 충분합니다. 여유 공간: {free_space_mb:.2f} MB, 필요 공간: {required_capacity_mb} MB")
                return
            
            self.logger.info(f"디스크 공간 부족. 여유 공간: {free_space_mb:.2f} MB, 필요 공간: {required_capacity_mb} MB")
            
            # 팝업이 이미 표시되어 있지 않은 경우에만 새 팝업 생성
            if self._disk_warning_dialog is None or not self._disk_warning_dialog.isVisible():
                self._disk_warning_dialog = QMessageBox()
                self._disk_warning_dialog.setIcon(QMessageBox.Warning)
                self._disk_warning_dialog.setWindowTitle("디스크 공간 부족")
                self._disk_warning_dialog.setText(f"현재 저장공간 부족으로 인해 저장 파일을 삭제합니다.")
                self._disk_warning_dialog.setStandardButtons(QMessageBox.Ok)
                self._disk_warning_dialog.setModal(True)
                self._disk_warning_dialog.show()
            
            # 2초 후 파일 삭제 시작
            QTimer.singleShot(2000, lambda: self._perform_file_deletion(root_dir))
            
        finally:
            # 함수 종료 시 실행 상태 해제 (팝업은 유지)
            self._check_and_free_space_running = False

    def _perform_file_deletion(self, root_dir):
        """
        실제 파일 삭제 작업을 수행하는 함수
        별도의 running 변수로 중복 실행 방지
        """
        # 이미 삭제 작업이 실행 중인 경우 함수 종료
        if self._perform_file_deletion_running:
            self.logger.info("_perform_file_deletion 함수가 이미 실행 중입니다.")
            return
        
        # 삭제 작업 실행 상태를 True로 설정
        self._perform_file_deletion_running = True
        
        try:
            # 설정값 다시 읽기
            required_capacity_mb = int(self.setting.get("required_capacity", "100", group="자동 정리 설정"))
            delete_capacity_mb = int(self.setting.get("delete_capacity", "500", group="자동 정리 설정"))
            
            # 대상 디렉토리: img와 video
            target_dirs = [
                os.path.join(root_dir, "img"),
                os.path.join(root_dir, "video")
            ]
            
            # while 루프를 통해 필요한 용량이 확보될 때까지 삭제 작업 반복
            total_deleted_files = 0
            total_freed_space = 0
            
            while True:
                # 현재 디스크 사용량 재확인
                usage = shutil.disk_usage(root_dir)
                free_space = usage.free
                free_space_mb = free_space / (1024 * 1024)
                
                # 필요한 용량이 확보되었는지 확인
                if free_space_mb >= required_capacity_mb:
                    self.logger.info(f"필요한 용량 확보 완료: {free_space_mb:.2f} MB >= {required_capacity_mb} MB")
                    break
            
                # 삭제할 파일 목록 수집
                files = []
                for target_dir in target_dirs:
                    if os.path.exists(target_dir):
                        for subdir, _, filenames in os.walk(target_dir):
                            for filename in filenames:
                                file_path = os.path.join(subdir, filename)
                                files.append((file_path, os.path.getmtime(file_path), os.path.getsize(file_path)))
                    else:
                        self.logger.warning(f"디렉토리 {target_dir}가 존재하지 않습니다.")
                
                if not files:
                    self.logger.error("삭제할 파일이 없으나 디스크 공간이 부족합니다!")
                    break
                
                # 수정 시간 기준으로 정렬 (가장 오래된 파일 먼저)
                files.sort(key=lambda x: x[1])
                
                # delete_capacity_mb만큼 파일 삭제
                delete_capacity_bytes = delete_capacity_mb * 1024 * 1024
                freed_space = 0
                deleted_files = 0
                
                for file_path, _, file_size in files:
                    if freed_space >= delete_capacity_bytes:
                        break  # 이번 라운드에서 충분한 공간 확보
                    try:
                        os.remove(file_path)
                        freed_space += file_size
                        deleted_files += 1
                        self.logger.info(f"삭제 완료: {file_path} ({file_size / (1024 * 1024):.2f} MB)")
                    except Exception as e:
                        self.logger.error(f"{file_path} 삭제 실패: {e}")
                
                total_deleted_files += deleted_files
                total_freed_space += freed_space
                
                self.logger.info(f"이번 라운드: {deleted_files}개 파일, {freed_space / (1024 * 1024):.2f} MB 공간 확보")
                
                # 이번 라운드에서 삭제된 파일이 없으면 무한 루프 방지를 위해 종료
                if deleted_files == 0:
                    self.logger.warning("더 이상 삭제할 수 있는 파일이 없습니다.")
                    break
        
        finally:
            # 삭제 작업 종료 시 실행 상태 해제
            self._perform_file_deletion_running = False
  
        self.logger.info(f"전체 삭제 완료: 총 {total_deleted_files}개 파일, {total_freed_space / (1024 * 1024):.2f} MB 공간 확보")

    def _reconnect_all_cctv_streams(self):
        """모든 CCTV 스트림 재연결 시도"""
        if hasattr(self, "background_controller"):
            self.background_controller.reconnect_all_streams()

    @Slot(dict)
    def video_control(self, clicked_cctv_info: dict):
        """
        PTZ 카메라 제어용 함수

        개별 CCTV 클릭 시 호출되며, 클릭된 CCTV의 그리드 인덱스와 비디오 URL을 출력합니다.

        Parameters
        ----------
        clicked_cctv_info : dict
            다음 요소를 포함하는 딕셔너리:
            - camera_id : int
                선택된 CCTV의 ID (DB에 등록된 ID)
            - camera_name : str
                선택된 CCTV의 이름
            - camera_ip : str
                CCTV와 관련된 비디오 스트림의 IP
                RTSP 연결용 포트
            - rtsp_id : int
                RTSP 연결용 ID
            - rtsp_pw : int
                RTSP 연결용 PW
            - port : int
            - video_num
                CCTV가 위치한 그리드의 인덱스
                

        {'camera_id': 1, 'camera_ip': '192.168.88.20', 'camera_name': 'CCTV 1', 'port': 8554, 'rtsp_id': '', 'rtsp_pw': '', 'video_num': 3}

        """
        # self.logger.info(f"clicked_cctv_info: {clicked_cctv_info}")
        self.clicked_cctv_info = clicked_cctv_info
        if not self.is_layout_modify:
            if clicked_cctv_info:
                self.ptz_controller_widget.setup_ptz_controls(clicked_cctv_info["camera_ip"], clicked_cctv_info["ptz_port"], clicked_cctv_info["rtsp_id"], clicked_cctv_info["rtsp_pw"])
    
    # 레이아웃 재생 관련 함수
    @Slot(dict)
    def get_layout_data_and_play_all_cctv_stream_in_layout_data(self, grid_data: dict):
        video_data_list: list[dict] = json.loads(grid_data['video_data'])
        self.current_video_layout_name: str = grid_data['name']
        current_tab_index = self.tab_widget_video_player.currentIndex()
        video_player_widget = self.video_player_widget_list[current_tab_index]

        # 비디오 플레이어 위젯 초기화
        video_player_widget.is_grid_creating = False
        video_player_widget.clear_grid_widget()

        def play_layout():
            if not video_data_list:
                return

            # 레이아웃 데이터 기반 그리드 생성
            video_data_list_copy = video_data_list.copy()
            max_position_data = max(video_data_list_copy, key=lambda x: x.get("position", [0, 0])[0], default=None)
            if max_position_data:
                max_x, max_y = max_position_data.get("position", [0, 0])
                video_player_widget.create_grid(max_x + 1)

            # 백그라운드 비디오 목록 가져오기
            background_video_list = self.background_controller.get_video_list()

            # video_data_list의 각 항목 처리
            for video_data in video_data_list:
                cctv_info = video_data.get("cctv_info", {})
                position = video_data.get("position", [0, 0])  # [row, col]
                target_position = tuple(position)  # (row, col) 튜플로 변환
                camera_info = cctv_info.get("camera_info", {})
                camera_id = camera_info.get("id", -1)
                camera_name = camera_info.get("camera_name", "Unknown")

                if camera_id == -1:
                    self.logger.error("카메라 ID가 지정되지 않았습니다.")
                    continue

                # 백그라운드에서 해당 카메라 ID로 실행 중인 프로세스 찾기
                existing_video_config = None
                for config in background_video_list:
                    if config.camera_info.get("id") == camera_id:
                        existing_video_config = config
                        break

                if existing_video_config:
                    video_player_widget.play(existing_video_config, True, target_position)
                    QTimer.singleShot(1000, lambda config=existing_video_config: self.activate_visualization(config))

            # 탭 데이터 저장
            self.tab_data[current_tab_index] = video_data_list

        # clear_grid_widget 호출 후 UI가 업데이트될 시간을 확보하기 위해 singleShot 사용
        QTimer.singleShot(0, play_layout)

    @Slot(EventLogData)
    def on_event_log_received(self, event_log: EventLogData):
        """
        이벤트 로그 수신 시 호출되는 슬롯 함수
        
        예시:
        EventLogData(
            timestamp=1750140246.7525249,
            cctv_location='1공장',
            cctv_name='CCTV 2',
            event_name='사람과 차',
            image_path='/home/rist/rist-ai-cctv-2025-2nd/img/2025-06-17/20250617_150406_CCTV 2.jpg'
            jiguk_performed=True
        )
        """
        # self.logger.info(event_log)
        self.ai_event_log_widget.add_event_log_to_table(event_log)
        self.ai_event_log_image_widget.add_event_log_image_to_scroll_area(event_log.image_path)
        self.snapshot_image_widget.add_event_log_image_to_scroll_area(event_log.image_path)
    @Slot(EventLogData)
    def on_event_status_changed(self, event_log: EventLogData):
        """
        이벤트 grid 변경을 위해 호출되는 슬롯 함수
        
        예시:
        EventLogData(
            timestamp=1750140246.7525249,
            cctv_location='1공장',
            cctv_name='CCTV 2',
            event_name='사람과 차',
            image_path='/home/rist/rist-ai-cctv-2025-2nd/img/2025-06-17/20250617_150406_CCTV 2.jpg'
        )
        """
        self.system_status_dialog.update_event_status(event_log)
        # 디스크 공간 체크 및 정리 실행
        self._check_and_free_space()

    @Slot(dict)
    def on_metrics_updated(self, metrics: dict):
        """
        BackgroundController로부터 필터링된 메트릭 데이터를 수신하는 슬롯 함수
        TODO: 수신된 metrics 데이터를 사용하여 UI 업데이트 또는 다른 로직 수행

        예시 출력:
        metrics = {
            'CCTV 1': { # CCTV 이름
                'client_side_frame_rate': 29.4,  # 클라이언트 측 프레임 속도
                'current_frame': 597,  # 현재 프레임 번호
                'original_fps': 30.0  # 원본 FPS                
                'assigned_events': {
                    '개구부 진입 감지': {
                        'ai_models': {
                            '05_gagubu': {
                                'client_side_rps': 10.7,
                                'estimated_rps': 10.0,
                                'gpu_id': 'GPU-29cee7ba-3d60-4839-8111-11b8d0f37f28',
                                'skip_frame': 3
                            }
                        }
                    }
                }
            }, ...
        }
        
        """
        # metrics 데이터가 비어있으면 아무것도 하지 않음
        if not metrics:
            return

        log_messages = ["\n========== 실시간 모니터링 현황 =========="]

        natural_sort_key = lambda s: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', s[0])]
        sorted_cctv_items = sorted(metrics.items(), key=natural_sort_key)
        total_rps = 0.0
        average_rps = 0.0

        for cctv_name, cctv_data in sorted_cctv_items:
            client_fps: float = cctv_data.get("client_side_frame_rate", 0.0)
            original_fps: float = cctv_data.get("original_fps", 0.0)

            if client_fps > original_fps:
                client_fps = original_fps

            cctv_log = [f"\n[{cctv_name}]"]
            cctv_log.append(f"  - 재생 성능: {client_fps:.1f} / {original_fps:.1f} FPS")

            assigned_events = cctv_data.get("assigned_events", {})
            if not assigned_events:
                cctv_log.append("  - (할당된 이벤트 없음)")
            else:
                cctv_log.append("  - AI 이벤트 성능 (실제/목표 RPS):")
                for event_name, event_data in assigned_events.items():
                    ai_models = event_data.get("ai_models", {})
                    total_client_rps: float = sum(model.get("client_side_rps", 0.0) for model in ai_models.values())
                    total_estimated_rps: float = sum(model.get("estimated_rps", 0.0) for model in ai_models.values())
                    if total_client_rps > total_estimated_rps:
                        total_client_rps = total_estimated_rps
                    cctv_log.append(f"    - {event_name}: {total_client_rps:.1f} / {total_estimated_rps:.1f} RPS")
                    total_rps += total_client_rps

            log_messages.append("\n".join(cctv_log))
        
        average_rps = total_rps / len(metrics) if metrics else 0.0
        log_messages.append(f"\n[전체 AI 이벤트 성능 합계]: {total_rps:.1f} RPS (평균: {average_rps:.1f} RPS)")
        log_messages.append("\n==========================================")

        # 콘솔 출력
        self.logger.info("\n".join(log_messages))

    #endregion

    #region 다이얼로그 관련 함수
    def toggle_event_log_image_widget(self):
        if self.ai_event_log_image_widget.isVisible():
            self.ai_event_log_image_widget.hide()
        else:
            self.ai_event_log_image_widget.show()

    def open_system_status_dialog(self):
        self.system_status_dialog.show()

    def open_ai_event_log_search_dialog(self):
        self.ai_event_log_search_dialog.show()

    def open_cctv_setting_dialog(self):
        # CCTV 설정 대화상자 열기
        self.cctv_setting_dialog.show()
        self.cctv_setting_dialog.load_cctv_list()
        
    def open_cctv_rpa_settings(self):
        self.rap_dialog.show()
    
    def open_auto_delete_settings_dialog(self):
        self.auto_delete_dialog.show()
    
    def open_event_logic_management_dialog(self):
        self.management_dialog.show()
        self.management_dialog.open_event_logic_management_dialog()
    
    def open_model_list_management_dialog(self):
        # AI 트레이닝 관리 대화상자 열기
        self.management_dialog.show()
        self.management_dialog.open_model_list_management_dialog()

    def open_cctv_management_dialog(self):
        # CCTV 관리 대화상자 열기
        self.management_dialog.show()
        self.management_dialog.open_cctv_management_dialog()
    #endregion

    def closeEvent(self, event):
        """애플리케이션 종료 시 발생하는 이벤트 핸들러"""

        if hasattr(self, 'background_controller'):
            self.background_controller.stop_all_processes()

        if self.rap_dialog:
            self.rap_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.rap_dialog.close()

        if self.system_status_dialog:
            self.system_status_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.system_status_dialog.close()
            
        event.accept()

if __name__ == "__main__":
    mp.set_start_method('spawn', force=True) 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.play_all_cctv_streams()
    sys.exit(app.exec())
    # exec() :창 송출 시 다른 창과의 상호작용 차단 / show() :창 송출 시에도 다른 창과의 상호작용 허용