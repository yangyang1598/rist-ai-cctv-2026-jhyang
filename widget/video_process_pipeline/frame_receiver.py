# frame_receiver.py
import numpy as np
import multiprocessing as mp
import queue
import gc
import torch
from PySide6.QtCore import QThread, Signal, QTimer, Slot
from PySide6.QtGui import QImage
from setting import paths
from setting.use_qsetting import Setting
from widget.video_process_pipeline.video_config import FrameData, EventGridData, PerformanceData, VideoConfig, setup_logger, EventLogData


SETTING_DICT: dict =  Setting(paths.GLOBAL_SETTING_PATH).to_dict()
GLOBAL_SETTING: dict = SETTING_DICT.get("global", {})
SYSTEM_CHECK_TIME = int(GLOBAL_SETTING.get("system_check_time", 60))

class FrameReceiver(QThread):
    frame_received = Signal(VideoConfig, QImage)
    performance_data_received = Signal(PerformanceData)
    event_log_received = Signal(EventLogData)
    event_status_received = Signal(EventLogData)
    stream_status_received = Signal(dict)

    def __init__(self, output_queue: queue.Queue, event_grid_queue: queue.Queue, parent=None):
        super().__init__(parent)
        self.output_queue = output_queue
        self.event_grid_queue = event_grid_queue
        self.running = False
        self.logger = setup_logger("FrameReceiver")
        # self._frame_count = 0
        # self._drop_count = 0

        self.queue_check_timer = QTimer()
        self.queue_check_timer.timeout.connect(self.gc_collect_and_clear_resource)
        self.queue_check_timer.start(60 * 1000)  # 1분 마다 큐를 확인
        
        # self.status_check_timer = QTimer()
        # self.status_check_timer.timeout.connect(self.status_check)
        # self.status_check_timer.start(10 * 1000)

    @Slot()
    def gc_collect_and_clear_resource(self):
        gc.collect()
        torch.cuda.empty_cache()
        while not self.output_queue.empty():
            try:
                data: FrameData = self.output_queue.get_nowait()
                del data
            except queue.Empty:
                break # 큐가 비었으면 루프 종료

    @Slot()
    def status_check(self):
        if self.isRunning():
            self.logger.info("프레임 리시버 On")
        else:
            self.logger.info("프레임 리시버 Off")

    def run(self):
        self.running = True
        
        while self.running:
            try:
                data = self.output_queue.get(timeout=0.1)

                # 스트림 상태 메시지 처리
                if isinstance(data, dict) and data.get("type") == "stream_status":
                    self.stream_status_received.emit(data)
                    continue

                if isinstance(data, FrameData):
                    frame_data: FrameData = data

                    if frame_data.is_event_notification:
                        self.event_log_received.emit(frame_data.event_log)
                    
                    if frame_data.frame is not None:
                        q_image = self._convert_to_qimage(frame_data.frame)
                        if q_image is not None:
                            self.frame_received.emit(frame_data.cctv_info, q_image)
                            del q_image
                            # self._frame_count += 1
                        # else:
                            # self._drop_count += 1

                elif isinstance(data, PerformanceData):
                    perf_data: PerformanceData = data
                    self.performance_data_received.emit(perf_data)
                    continue

                # 이벤트 그리드 큐에서 데이터를 가져오되, 비어있지 않은 경우에만 시도
                if not self.event_grid_queue.empty():
                    try:
                        grid_data: EventGridData = self.event_grid_queue.get_nowait()
                        if grid_data.display_event is not None:
                            # self.logger.info(f"Grid Data Event Log: {grid_data.display_event}")
                            self.event_status_received.emit(grid_data.display_event)
                    except queue.Empty:
                        pass  # 큐가 비어있으면 그냥 넘어감

            except queue.Empty:
                continue
                
            except Exception as e:
                self.logger.error(f"프레임 수신 중 오류: {e}")
                # self._drop_count += 1
        
    def _convert_to_qimage(self, frame: np.ndarray):
        try:
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            return q_image
            
        except Exception as e:
            self.logger.error(f"QImage 변환 실패: {e}")
            return None
    
    def stop(self):
        self.logger.info("프레임 수신 종료 요청")
        self.running = False
        
        # 스레드 종료 대기
        if not self.wait(2000):  # 2초 대기
            self.logger.warning("프레임 수신 스레드 종료 시간 초과")
            self.terminate()
            self.wait()
