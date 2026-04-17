# video_writer.py
import queue
import threading
import cv2
import numpy as np
from setting import paths
from setting.use_qsetting import Setting
from widget.video_process_pipeline.video_config import setup_logger


GLOBAL_SETTING: dict = Setting(paths.GLOBAL_SETTING_PATH).to_dict().get("global", {}) 
RECORD_DURATION: float = float(GLOBAL_SETTING.get("record_duration", 5.0))  # 초 단위

class VideoWriter:
    def __init__(self, output_path: str, frame_size: tuple):
        self.logger = setup_logger("VideoWriter")
        self.output_path = output_path
        self.frame_size = (1920, 1080) # if frame_size is None else frame_size
        self.frame_queue = queue.Queue(maxsize=100)
        self.writer_thread = None
        self.is_recording = False
        self.video_writer = None
        
    def start_recording(self):
        """녹화 시작"""
        if not self.is_recording:
            self.is_recording = True
            self.writer_thread = threading.Thread(target=self._video_writing_loop, daemon=True, name="StartRecordingThread")
            self.writer_thread.start()

            # TODO: 녹화 지속 시간 설정을 설정할 수 있도록 변경해야함
            stop_timer = threading.Timer(RECORD_DURATION, self.stop_recording)
            stop_timer.start()
    
    def add_frame(self, frame_bgr: np.ndarray):
        """프레임 추가 (BGR 형식)"""
        if self.is_recording:
            try:
                self.frame_queue.put_nowait(frame_bgr)
            except queue.Full:
                # 큐가 가득 찬 경우 가장 오래된 프레임 제거 후 추가
                try:
                    self.frame_queue.get_nowait()
                    self.frame_queue.put_nowait(frame_bgr)
                except queue.Empty:
                    pass
    
    def stop_recording(self):
        """녹화 중지"""
        if self.is_recording:
            self.is_recording = False
            # 종료 신호 전송
            self.frame_queue.put(None)
            
            # 스레드 종료 대기
            if self.writer_thread and self.writer_thread.is_alive():
                self.writer_thread.join(timeout=5.0)
                if self.writer_thread.is_alive():
                    # 강제 종료가 필요한 경우 로그 출력
                    self.logger.warning(f"비디오 스레드가 정상적으로 종료되지 않음: {self.output_path}")

            while not self.frame_queue.empty():
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    break

    def _video_writing_loop(self):
        """비디오 작성 루프"""
        try:
            # VideoWriter 초기화
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                self.output_path, 
                fourcc, 
                30.0,  # FPS
                self.frame_size
            )
            
            if not self.video_writer.isOpened():
                self.logger.warning(f"비디오 파일 생성 실패: {self.output_path}")
                return
            
            # frame_count = 0
            while self.is_recording:
                try:
                    frame = self.frame_queue.get(timeout=1.0)
                    
                    # 종료 신호 확인
                    if frame is None:
                        break
                    
                    # 프레임 크기 조정 (필요한 경우)
                    frame = cv2.resize(frame, self.frame_size)
                    
                    self.video_writer.write(frame)
                    # frame_count += 1
                    
                except queue.Empty:
                    # 타임아웃 발생 시 계속 진행
                    continue
                except Exception as e:
                    self.logger.warning(f"프레임 작성 오류: {e}")
                    break
            
            # print(f"비디오 저장 완료: {self.output_path} (총 {frame_count}프레임)")
            
        except Exception as e:
            self.logger.warning(f"비디오 작성 루프 오류: {e}")
        finally:
            # 리소스 정리
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None