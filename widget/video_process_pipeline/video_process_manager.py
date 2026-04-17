# process_manager.py
import time
import multiprocessing as mp
import queue
from typing import Dict, Set, List
from widget.video_process_pipeline.video_config import VideoConfig, MessageType, setup_logger
from widget.video_process_pipeline.video_process import video_process_main


class ProcessManager:
    def __init__(self, output_queue: queue.Queue, event_grid_queue: queue.Queue, logger=None):
        self.output_queue = output_queue
        self.event_grid_queue = event_grid_queue    
        self.logger = logger or setup_logger("ProcessManager")
        
        # 프로세스와 통신 채널 관리
        self.processes: Dict[int, mp.Process] = {}
        self.command_queues: Dict[int, mp.Queue] = {}
        
        # 상태 추적
        self.active_videos: Set[int] = set()
        self.active_camera_list: Dict[int, str] = {}
        self._gpu_assignment: Dict[int, int] = {}  # video_id -> gpu_id
        self.stream_health_status: Dict[int, bool] = {}  # 스트림 상태 추적

    def create_video_process(self, config: VideoConfig) -> bool:
        camera_id = config.camera_info.get('id', None)
        camera_name = config.camera_info.get('camera_name', None)
        camera_location = config.camera_info.get('camera_location', None)
        video_id = config.video_number
        
        try:
            # 명령 큐 생성 - 각 프로세스마다 독립적인 큐
            command_queue = mp.Queue(maxsize=5)
            self.command_queues[video_id] = command_queue
            
            # 프로세스 생성
            process = mp.Process(
                target=video_process_main,
                args=(config, command_queue, self.output_queue,self.event_grid_queue),
                daemon=True,  # 메인 프로세스 종료 시 함께 종료
                name=f"VideoProcess-{video_id}"
            )
            
            process.start()
            self.processes[video_id] = process
            self.active_videos.add(video_id)
            self.active_camera_list[video_id] = {'camera_id': camera_id, 'camera_location': camera_location, 'camera_name': camera_name}
            self.stream_health_status[video_id] = True
            self._gpu_assignment[video_id] = config.device
            
            self.logger.info(f"[{camera_name}] Video {video_id} 프로세스 생성 성공 (PID: {process.pid}, GPU: {config.device})")
            return True
            
        except Exception as e:
            self.logger.error(f"[{camera_name}] Video {video_id} 프로세스 생성 실패: {e}")
            if video_id in self.command_queues:
                del self.command_queues[video_id]
            
            return False
    
    def create_batch_processes(self, configs: List[VideoConfig], batch_size: int = 10, delay: float = 0.5) -> int:
        created_count = 0
        total_configs = len(configs)
        
        self.logger.info(f"{total_configs}개 프로세스를 {batch_size}개씩 배치로 생성합니다")
        
        for i in range(0, total_configs, batch_size):
            batch = configs[i:i + batch_size]
            batch_created = 0
            
            for config in batch:
                if self.create_video_process(config):
                    batch_created += 1
                    created_count += 1
            
            self.logger.info(f"배치 {i//batch_size + 1}/{(total_configs + batch_size - 1)//batch_size} 완료: {batch_created}/{len(batch)} 프로세스 생성")

            if i + batch_size < total_configs:
                import time
                time.sleep(delay)
        return created_count
    
    def send_command(self, video_id: int, message: dict) -> bool:
        if video_id not in self.command_queues:
            self.logger.error(f"Video {video_id}: 명령 큐가 존재하지 않습니다")
            return False
        
        try:
            self.command_queues[video_id].put_nowait(message)
            return True
            
        except queue.Full:
            self.logger.warning(f"Video {video_id}: 명령 큐가 가득 찼습니다")
            try:
                old = self.command_queues[video_id].get_nowait()
                del old
                self.command_queues[video_id].put_nowait(message)
            except queue.Empty:
                pass
            return True
        
        except Exception as e:
            self.logger.error(f"Video {video_id}: 명령 전송 실패 - {e}")
            return False
    
    def broadcast_command(self, message: dict, video_ids: List[int] = None):
        targets = video_ids if video_ids is not None else list(self.active_videos)
        
        success_count = 0
        for video_id in targets:
            if self.send_command(video_id, message):
                success_count += 1
        
        self.logger.info(f"브로드캐스트 완료: {success_count}/{len(targets)} 프로세스에 전송")
    
    def stop_process(self, video_id: int, timeout: float = 3.0) -> bool:
        if video_id not in self.processes:
            self.logger.warning(f"Video {video_id}: 프로세스가 존재하지 않습니다")
            return False
        
        # 종료 명령 전송
        self.send_command(video_id, {'type': MessageType.SHUTDOWN})
        
        # 프로세스 종료 대기
        process = self.processes[video_id]
        pid = process.pid
        process.join(timeout=timeout)
        
        # 타임아웃 시 강제 종료
        if process.is_alive():
            self.logger.warning(f"Video {video_id}: 정상 종료 실패, 강제 종료 시도")
            process.terminate()
            process.join(timeout=1.0)
            
            if process.is_alive():
                self.logger.error(f"Video {video_id}: 강제 종료 실패")
                return False
        
        # 정리
        del self.processes[video_id]
        del self.command_queues[video_id]
        self.active_videos.discard(video_id)
        del self.active_camera_list[video_id]
        if video_id in self._gpu_assignment:
            del self._gpu_assignment[video_id]
        
        self.logger.info(f"Video {video_id}: 프로세스 종료 완료 (PID: {pid})")
        return True
    
    def stop_all(self, timeout: float = 5.0):
        if not self.active_videos:
            self.logger.info("종료할 프로세스가 없습니다")
            return
        
        # self.logger.info(f"{len(self.active_videos)}개 프로세스 종료 시작...")
        
        # 모든 프로세스에 종료 명령 전송
        shutdown_message = {'type': MessageType.SHUTDOWN}
        self.broadcast_command(shutdown_message)
        
        # 프로세스별 종료 대기
        remaining_time = timeout
        for video_id in list(self.active_videos):
            start_time = time.time()
            self.stop_process(video_id, timeout=remaining_time)
            remaining_time -= (time.time() - start_time)
            
            if remaining_time <= 0:
                break
        
        # 남은 프로세스 강제 종료
        for video_id in list(self.active_videos):
            process = self.processes.get(video_id)
            if process and process.is_alive():
                self.logger.warning(f"Video {video_id}: 강제 종료")
                process.terminate()
        
        # 최종 정리
        self.processes.clear()
        self.command_queues.clear()
        self.active_videos.clear()
        self.active_camera_list.clear()
        self._gpu_assignment.clear()
        
        self.logger.info("모든 프로세스 종료 완료")

    def reconnect_all_streams(self):
        """모든 스트림에 재연결 명령 전송"""
        if not self.active_videos:
            self.logger.info("재연결할 프로세스가 없습니다")
            return
        
        self.logger.info(f"{len(self.active_videos)}개 프로세스에 재연결 명령 전송")
        reconnect_message = {'type': MessageType.RECONNECT}
        self.broadcast_command(reconnect_message)

    def is_process_running(self, video_id: int) -> bool:
        """특정 비디오 프로세스가 실행 중인지 확인"""
        if video_id not in self.processes:
            return False
        return self.processes[video_id].is_alive()
    
    def update_stream_health(self, video_id: int, is_healthy: bool):
        """스트림 상태 업데이트"""
        self.stream_health_status[video_id] = is_healthy
        # if not is_healthy:
        #     self.logger.warning(f"Video {video_id} 스트림 비정상 상태")

    def is_stream_healthy(self, video_id: int) -> bool:
        """스트림이 정상 상태인지 확인"""
        return self.stream_health_status.get(video_id, False)

    def get_healthy_process_count(self) -> int:
        """정상 상태의 프로세스 수 반환"""
        count = 0
        for video_id in self.active_videos:
            process = self.processes.get(video_id)
            is_alive = process and process.is_alive() and process.exitcode is None
            is_healthy = self.stream_health_status.get(video_id, False)
            if is_alive and is_healthy:
                count += 1
        return count