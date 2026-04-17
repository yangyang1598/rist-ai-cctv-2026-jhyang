# video_player_widget.py
from typing import Dict
from PySide6.QtWidgets import QWidget, QGridLayout, QMessageBox, QSizePolicy
from PySide6.QtCore import Slot, Signal, QEvent
from PySide6.QtGui import QImage
from widget.video_process_pipeline.video_config import VideoConfig, LayoutData, setup_logger, MessageType
from widget.video_process_pipeline.video_display_widget import VideoDisplayWidget
from rich.console import Console
console = Console()

class VideoPlayerWidget(QWidget):
    clicked_cctv_info = Signal(dict)
    current_layout_data = Signal(LayoutData)

    def __init__(self, player_index: int = 0, main_window=None):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_window = main_window  # MainWindow 참조 저장
        self.logger = setup_logger("VideoPlayerWidget")
        self.player_widget_index: int = player_index
        self.video_widgets: Dict[int, VideoDisplayWidget] = {}
        self.grid: int = 1
        self.is_grid_creating: bool = False
        self.is_layout_modify_mode: bool = False
        self.first_selected_index_for_swap: int = -1
        self.selected_grid_index: int = -1
        self.grid_video_mapping = {}
        self.temp_layout_data: LayoutData = None

    def create_grid(self, display_type: int):
        """비디오 디스플레이 그리드를 생성합니다."""
        # self.logger.info(f"Creating grid with display type: {display_type}")

        if display_type <= 5:
            self.grid_row = display_type
            self.grid_col = display_type
        else:
            self.grid_row = 8
            self.grid_col = 9

        self.init_grid()
        self.update()

        # # 프레임 수신기 초기화 (한 번만)
        # if not hasattr(self, 'output_queue'):
        #     self.output_queue = mp.Queue(maxsize=72)
        #     # self.output_queue = queue.Queue(50)
        #     self.process_manager = ProcessManager(self.output_queue, self.logger)
        
        # # 프레임 수신기 연결 (한 번만)
        # if not hasattr(self, 'frame_receiver') or not self.frame_receiver.isRunning():
        #     self.frame_receiver = FrameReceiver(self.output_queue)
        #     self.frame_receiver.frame_received.connect(self.on_frame_received)
        #     self.frame_receiver.start()

    def init_grid(self):
        if hasattr(self, "grid_layout") and self.grid_layout:
            self.is_grid_creating = False
            self.clear_grid_widget()
        
        self.is_grid_creating = True
        self.create_grid_widget()

    def clear_grid_widget(self):
        if hasattr(self, "grid_layout") and self.grid_layout:
            self.is_grid_creating = False
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)
                widget = item.widget()

                if widget and isinstance(widget, VideoDisplayWidget):
                    video_number = widget.video_id

                    # self.main_window가 존재하고 background_controller 속성이 있는지 확인
                    if self.main_window and hasattr(self.main_window, 'background_controller'):
                        if video_number in [vc.video_number for vc in self.main_window.background_controller.get_video_list()]:
                            self.main_window.background_controller.process_manager.send_command(
                                video_number,
                                {'type': MessageType.UPDATE_VISUALIZATION, 'is_visualize': False}
                            )
                widget.deleteLater()

            if self.main_window and hasattr(self.main_window, 'background_controller'):
                self.main_window.background_controller.disconnect()
                self.grid_video_mapping = {}

            self.grid_layout.deleteLater()
            self.grid_layout = None
            self.video_widgets.clear()
            self.setLayout(None)
            # self.process_manager.stop_all() # <-- 모든 비디오 프로세스 
            # self.frame_receiver.stop()

    def create_grid_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        parent_widget = self.parent()
        if parent_widget:
            available_width = parent_widget.width()
            available_height = parent_widget.height()
        else:
            available_width = self.width()
            available_height = self.height()

        spacing = self.grid_layout.spacing()
        cell_width = (available_width - spacing * (self.grid_col - 1)) // self.grid_col
        cell_height = (available_height - spacing * (self.grid_row - 1)) // self.grid_row

        # 캐시된 값만 저장
        self.cached_cell_width = cell_width
        self.cached_cell_height = cell_height

        for row in range(self.grid_row):
            for col in range(self.grid_col):
                cell_widget = QWidget()
                cell_widget.setMinimumSize(0, 0)
                cell_widget.setStyleSheet("background-color: #333; border: 1px solid #555;")
                cell_widget.installEventFilter(self)

                self.grid_layout.setRowStretch(row, 1)
                self.grid_layout.setColumnStretch(col, 1)

                self.grid_layout.addWidget(cell_widget, row, col)
                widget_index = row * self.grid_col + col
                self.video_widgets[widget_index] = cell_widget
        self.setLayout(self.grid_layout)

        if self.main_window and hasattr(self.main_window, 'background_controller'):
            self.main_window.background_controller.connect()

    def calculate_empty_cell(self):
        for row in range(self.grid_row):
            for col in range(self.grid_col):
                index = row * self.grid_col + col
                widget = self.video_widgets.get(index)
                if widget and not isinstance(widget, VideoDisplayWidget):
                    return row, col
                
    def get_empty_cell_position(self) -> tuple[int, int] | None:
        """빈 그리드 위치(row, col)를 반환합니다."""
        try:
            empty_cell = self.calculate_empty_cell()
            if empty_cell is None:
                self.logger.warning("No empty cell found.")
                QMessageBox.information(self, "빈 그리드 셀 없음", "현재 빈 그리드 셀이 없습니다. \n상단의 버튼을 눌러 그리드를 초기화 해주세요.")
                return None
            else: 
                return empty_cell
        except Exception as e:
            print(f"Error finding empty cell position: {e}")
            return None

    #region 레이아웃 수정 모드 관련 함수
    def set_layout_modify_mode(self, is_modify: bool):
        """레이아웃 수정 모드를 설정합니다."""
        self.is_layout_modify_mode = is_modify
        self.first_selected_index_for_swap = -1
        self._clear_outline(self.selected_grid_index)
        self.selected_grid_index = -1

    def move_widget(self, index1: int, index2: int):
        """두 위젯의 위치를 교체하거나 빈 셀로 이동합니다."""
        widget1 = self.video_widgets.get(index1)
        widget2 = self.video_widgets.get(index2)

        is_widget1_video = isinstance(widget1, VideoDisplayWidget)
        is_widget2_video = isinstance(widget2, VideoDisplayWidget)

        if not is_widget1_video:
            self.logger.warning("첫 번째 선택은 비디오 위젯이어야 합니다.")
            return

        row1, col1 = index1 // self.grid_col, index1 % self.grid_col
        row2, col2 = index2 // self.grid_col, index2 % self.grid_col

        # 레이아웃에서 위젯 제거
        self.grid_layout.removeWidget(widget1)
        if widget2:
            self.grid_layout.removeWidget(widget2)

        # 경우에 따라 위젯을 레이아웃에 다시 추가
        if is_widget1_video and is_widget2_video: # 1. 둘 다 비디오 위젯 -> 교체
            self.grid_layout.addWidget(widget1, row2, col2)
            self.grid_layout.addWidget(widget2, row1, col1)
            self.video_widgets[index1], self.video_widgets[index2] = widget2, widget1
            widget1.video_id, widget2.video_id = widget2.video_id, widget1.video_id
            
            if index1 in self.grid_video_mapping and index2 in self.grid_video_mapping:
                self.grid_video_mapping[index1], self.grid_video_mapping[index2] = self.grid_video_mapping[index2], self.grid_video_mapping[index1]
                if hasattr(self, 'background_to_grid_mapping'):
                    bg1 = self.grid_video_mapping[index1]
                    bg2 = self.grid_video_mapping[index2]
                    self.background_to_grid_mapping[bg1] = index1
                    self.background_to_grid_mapping[bg2] = index2

        elif is_widget1_video and not is_widget2_video: # 2. 비디오 위젯을 빈 셀로 -> 이동
            self.grid_layout.addWidget(widget1, row2, col2)
            self.grid_layout.addWidget(widget2, row1, col1)
            widget2.setStyleSheet("background-color: #333; border: 1px solid #555;")
            widget1.video_id = index2
            self.video_widgets[index1], self.video_widgets[index2] = self.video_widgets[index2], self.video_widgets[index1]

            if index1 in self.grid_video_mapping:
                background_video_number = self.grid_video_mapping[index1]
                self.grid_video_mapping[index2] = background_video_number
                del self.grid_video_mapping[index1]
                
                if hasattr(self, 'background_to_grid_mapping'):
                    self.background_to_grid_mapping[background_video_number] = index2

    def remove_video_widget(self, index: int):
        """지정된 인덱스의 비디오 위젯을 제거하고 빈 셀로 만듭니다."""
        widget = self.video_widgets.get(index, None)
        if widget:
            if isinstance(widget, VideoDisplayWidget):
                if self.main_window and hasattr(self.main_window, 'background_controller'):
                    background_video_number = self.grid_video_mapping.get(index)
                    if background_video_number is not None:
                        self.main_window.background_controller.process_manager.send_command(
                            background_video_number,
                            {'type': MessageType.UPDATE_VISUALIZATION, 'is_visualize': False}
                        )

                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

                empty_widget = QWidget()
                empty_widget.setMinimumSize(0, 0)
                empty_widget.setStyleSheet("background-color: #333; border: 1px solid #555;")
                empty_widget.installEventFilter(self)

                row, col = index // self.grid_col, index % self.grid_col
                self.grid_layout.addWidget(empty_widget, row, col)
                self.video_widgets[index] = empty_widget

                if index in self.grid_video_mapping:
                    background_video_number = self.grid_video_mapping[index]
                    del self.grid_video_mapping[index]
                    
                    if hasattr(self, 'background_to_grid_mapping') and background_video_number in self.background_to_grid_mapping:
                        del self.background_to_grid_mapping[background_video_number]
            else:
                self.logger.warning("지정된 인덱스에 비디오 위젯이 없습니다.")
    #endregion

    @Slot(VideoConfig)
    def play(self, cctv_info: VideoConfig, is_exist_background: bool = False, target_position: tuple[int, int] = None):
        """
        CCTV 클릭 시 URL을 받아 빈 그리드 위치에 VideoDisplayWidget을 추가하고 비디오 프로세스를 실행.
        """
        # 빈 그리드 위치 찾기 또는 지정된 위치 사용
        if target_position:
            row, col = target_position
            index = row * self.grid_col + col
            
            # 지정된 위치가 유효한지 확인
            if index >= len(self.video_widgets) or isinstance(self.video_widgets.get(index), VideoDisplayWidget):
                self.logger.error(f"지정된 위치 [{row},{col}] (인덱스 {index})가 유효하지 않거나 이미 사용 중입니다.")
                return
            
            position = (row, col)
            # self.logger.info(f"지정된 위치 사용: [{row},{col}] (인덱스 {index})")
        else:
            position = self.get_empty_cell_position()
            if not position:
                self.logger.error("No empty grid position available.")
                return
            row, col = position
            index = row * self.grid_col + col

        is_visualize: bool = cctv_info.is_visualize

        # 기존 백그라운드 비디오 재사용 시
        if is_exist_background:
            # 원본 백그라운드 프로세스의 video_number 보존
            original_video_number = cctv_info.video_number
            # 그리드에서는 인덱스를 video_number로 사용
            display_video_number = index
            # self.logger.info(f"백그라운드 재사용: 원본 video_number {original_video_number} -> 그리드 video_number {display_video_number}")
        else:
            # 새 비디오 프로세스 생성 시 그리드 인덱스를 video_number로 사용
            cctv_info.video_number = index
            original_video_number = index
            display_video_number = index
            gpu_id = 0 if index % 2 == 1 else 1  # 홀수: GPU0, 짝수: GPU1
            cctv_info.device = gpu_id

        # VideoDisplayWidget 생성 (그리드 인덱스를 video_number로 사용)
        video_widget = VideoDisplayWidget(display_video_number, cctv_info)
        video_widget.setMinimumSize(100, 100)
        if is_visualize:
            video_widget.setStyleSheet("background-color: #FFF; border: 1px solid #555;")
        else:
            video_widget.setStyleSheet("background-color: #333; border: 1px solid #555;")
        video_widget.is_cctv_clicked.connect(self.on_cctv_clicked)
        video_widget.is_cctv_double_clicked.connect(self.on_cctv_double_clicked)

        # 새로운 위젯을 추가하기 전, 기존의 플레이스홀더 위젯을 제거
        existing_widget = self.video_widgets.get(index)
        if existing_widget:
            self.grid_layout.removeWidget(existing_widget)
            existing_widget.deleteLater()

        self.grid_layout.addWidget(video_widget, row, col)
        self.video_widgets[index] = video_widget

        if not is_exist_background:
            # if not self.process_manager.is_process_running(cctv_info.video_number):
            #     self.process_manager.create_video_process(cctv_info)

            # self.process_manager.broadcast_command({
            #     'type': MessageType.UPDATE_VISUALIZATION,
            #     'is_visualize': is_visualize
            # }, [display_video_number])
            pass
        
        # 매핑: 그리드 인덱스 -> 실제 백그라운드 프로세스 video_number
        if not hasattr(self, 'background_to_grid_mapping'):
                self.background_to_grid_mapping = {}

        if is_exist_background:
            self.grid_video_mapping[index] = original_video_number # 원본 백그라운드 video_number
            # 추가 매핑 테이블 (백그라운드 -> 그리드 역방향 매핑용)
            self.background_to_grid_mapping[original_video_number] = index
        else:
            self.grid_video_mapping[index] = display_video_number # 그리드 인덱스와 동일
            # [수정] background_to_grid_mapping도 함께 업데이트
            self.background_to_grid_mapping[display_video_number] = index

        # self.logger.info(self.grid_video_mapping) # {0: 0, 1: 20, 2: 41, 3: 63} 비디오 인덱스: CCTV ID
        # self.logger.info(f"비디오 배치 완료: 위치[{row},{col}] 인덱스{index} -> 백그라운드 비디오{self.grid_video_mapping[index]}")

    @Slot(VideoConfig, QImage)
    def on_frame_received(self, cctv_info: VideoConfig, q_image: QImage):
        """
        프레임 수신 시 호출됩니다.

        def run(self):
            ...
            self.frame_received.emit(frame_data.video_id, q_image) <-이 부분에서 frame_data 자체 수신 할 예정
            ...

        프로세스 간 전송되는 프레임 데이터 양식:
        video_id: int (비디오 ID)
        frame: Optional[Any] = None  (프레임 데이터 (예: numpy 배열))
        detections: list = field(default_factory=list) (탐지 결과)
        timestamp: float = 0.0 (프레임 타임스탬프)

        frame_data.detections를 수신하여 탐지결과 처리
        """
        video_number = cctv_info.video_number
        for grid_idx, vid_num in self.grid_video_mapping.items():
            if vid_num == video_number and grid_idx in self.video_widgets:
                self.video_widgets[grid_idx].update_frame(q_image)
                break

    #region CCTV 영상 클릭 관련 함수
    @Slot(str)
    def on_cctv_clicked(self, clicked_cctv_info: dict):
        """
        PTZ 제어용 함수
        VideoDisplayWidget에서 CCTV 클릭 시 호출됩니다.
        """
        index = clicked_cctv_info["video_num"]

        # 그리드 수정 모드
        if self.is_layout_modify_mode:
            if self.first_selected_index_for_swap == -1: # 첫 번째 위젯 선택
                self.first_selected_index_for_swap = index
                self._set_outline(index)
                self.selected_grid_index = index
            else: # 두 번째 위젯 선택
                if self.first_selected_index_for_swap != index:
                    self.move_widget(self.first_selected_index_for_swap, index)
                # 선택 상태 초기화
                self._clear_outline(self.first_selected_index_for_swap)
                self._clear_outline(index)
                self.first_selected_index_for_swap = -1
                self.selected_grid_index = -1
                
        # PTZ 제어 모드
        else:
            # 기존 아웃라인 제거
            self._clear_outline(self.selected_grid_index)
            
            # 같은 CCTV 클릭 시 선택 해제
            if index == self.selected_grid_index:
                self.selected_grid_index = -1
                # PTZ 위젯에 정보 초기화 신호 전송
                self.clicked_cctv_info.emit({})
                return
            
            # 새로운 CCTV 선택
            self._set_outline(index)
            self.selected_grid_index = index

        self.clicked_cctv_info.emit(clicked_cctv_info)

    @Slot(dict)
    def on_cctv_double_clicked(self, double_clicked_cctv_info: dict):
        """
        영상 확대/축소 함수
        VideoDisplayWidget에서 CCTV 더블 클릭 시 호출됩니다.

        그리드 1x1 일 경우를 영상 확대로 정의함
        그리드가 2x2 이상일 때 1x1로 클릭된 영상만 보여주도록 변경

        2x2 -> 더블클릭 -> 1x1 (선택된 영상) -> 더블클릭 -> 2x2 (원래대로)

        LayoutData(
            row=2, 
            col=2, 
            grid=<PySide6.QtWidgets.QGridLayout(0x44bee8b0) at 0x76e67e4a0040>, 
            cctv_info={
                0: VideoConfig()
            }
        )
        """
        
        # self.logger.info("더블클릭 이벤트")

        # 1. n x m 그리드에서 1x1 화면으로 확대
        if self.grid_row > 1:
            self.temp_layout_data = self.get_current_layout_data()
            if not self.temp_layout_data:
                return

            selected_video_num = double_clicked_cctv_info.get("video_num")
            
            if self.grid_layout:
                # 모든 위젯 숨기기
                for index, widget in self.video_widgets.items():
                    widget.hide()

                # 모든 행/열의 stretch를 0으로 설정하여 기존 레이아웃 공간 분배를 무효화
                for i in range(self.temp_layout_data.row):
                    self.grid_layout.setRowStretch(i, 0)
                for i in range(self.temp_layout_data.col):
                    self.grid_layout.setColumnStretch(i, 0)

                # 선택된 위젯만 (0,0)에 위치시키고 보이게 함
                selected_widget = self.video_widgets.get(selected_video_num)
                if selected_widget:
                    # 선택된 위젯을 (0,0)으로 옮기고 해당 셀의 stretch를 1로 설정하여 공간을 모두 차지하게 함
                    self.grid_layout.addWidget(selected_widget, 0, 0, 1, 1)
                    self.grid_layout.setRowStretch(0, 1)
                    self.grid_layout.setColumnStretch(0, 1)
                    selected_widget.show()
                    self.logger.info(f"{selected_widget.video_id}번 비디오 위젯을 확대합니다.")

                # 확대된 상태이므로 grid_row, grid_col을 1로 설정
                self.grid_row = 1
                self.grid_col = 1
                self.grid_layout.update()

        # 2. 1x1 화면에서 원래 n x m 그리드로 복원
        else:
            if not self.temp_layout_data:
                # self.temp_layout_data가 없으면 pass ex) 처음부터 1x1이거나 빈 Cell을 클릭했을 때
                # self.logger.info("복원할 레이아웃 정보가 없습니다. (이미 원래 레이아웃이거나, 확대된 상태가 아님)")
                pass
            else:
                # self.logger.info("원래 레이아웃으로 복원합니다.")
                # 저장된 레이아웃 정보로 그리드 크기 복원
                self.grid_row = self.temp_layout_data.row
                self.grid_col = self.temp_layout_data.col

                # 모든 행/열의 stretch를 1로 복원
                for i in range(self.grid_row):
                    self.grid_layout.setRowStretch(i, 1)
                for i in range(self.grid_col):
                    self.grid_layout.setColumnStretch(i, 1)

                # 모든 위젯을 원래 위치로 복원하고 보이게 함
                for index, widget in self.video_widgets.items():
                    row = index // self.grid_col
                    col = index % self.grid_col
                    self.grid_layout.addWidget(widget, row, col)
                    widget.show()
                
                self.temp_layout_data = None # 임시 데이터 초기화
                self.grid_layout.update()

    def _clear_outline(self, index):
        if index is not None and index in self.video_widgets:
            widget = self.video_widgets[index]
            if isinstance(widget, VideoDisplayWidget):
                if widget.cctv_info and widget.cctv_info.is_visualize:
                     widget.setStyleSheet("background-color: #FFF; border: 1px solid #555;")
                else:
                     widget.setStyleSheet("background-color: #333; border: 1px solid #555;")
            else:
                # 일반 QWidget은 기본 스타일로 복원
                widget.setStyleSheet("background-color: #333; border: 1px solid #555;")

    def _set_outline(self, index):
        if self.is_layout_modify_mode:
            self.video_widgets[self.first_selected_index_for_swap].setStyleSheet("border: 3px solid blue;")
        else:
            if index in self.video_widgets:
                self.video_widgets[index].setStyleSheet("border: 3px solid yellow;")

    def eventFilter(self, obj, event):
        """
        이벤트 필터를 통해 마우스 클릭을 감지합니다.
        """
        # 첫 번째로 선택된 영상 위젯이 있고, 클릭된 것이 빈 셀(VideoDisplayWidget이 아닌 QWidget)일 경우
        if self.is_layout_modify_mode and event.type() == QEvent.Type.MouseButtonPress:
            # 클릭된 빈 위젯의 인덱스 찾기
            if self.first_selected_index_for_swap != -1 and isinstance(obj, QWidget) and not isinstance(obj, VideoDisplayWidget):
                for index, widget in self.video_widgets.items():
                    if widget == obj:
                        self.move_widget(self.first_selected_index_for_swap, index)
                        self._clear_outline(self.first_selected_index_for_swap)
                        self._clear_outline(index)
                        self.first_selected_index_for_swap = -1
                        self.selected_grid_index = -1
                        break
                    
        return super().eventFilter(obj, event)

    def send_current_layout_data(self):
        """
        현재 그리드 정보를 전송합니다.
        """
        layout_data = LayoutData(
            row=self.grid_layout.rowCount(),
            col=self.grid_layout.columnCount(),
            grid=self.grid_layout,
            cctv_info={k: v.cctv_info for k, v in self.video_widgets.items() if isinstance(v, VideoDisplayWidget)}
        )
        self.current_layout_data.emit(layout_data)
    
    def get_current_layout_data(self, is_change_layout: bool = False) -> LayoutData:
        """
        현재 레이아웃 데이터를 반환합니다.
        """
        if is_change_layout:
            return None
        
        layout_data: LayoutData = None
        
        if hasattr(self, "grid_layout"):
            if self.grid_layout is not None:
                layout_data = LayoutData(
                    row=self.grid_layout.rowCount(),
                    col=self.grid_layout.columnCount(),
                    grid=self.grid_layout,
                    cctv_info={k: v.cctv_info for k, v in self.video_widgets.items() if isinstance(v, VideoDisplayWidget)}
                )
                return layout_data
        else:
            return None
    
    def get_current_player_index(self) -> int:
        """
        현재 플레이어 인덱스를 반환합니다.
        """
        return self.player_widget_index
    #endregion    

