# main.py
import time
import re
import requests
import multiprocessing as mp
from collections import defaultdict
from typing import List, Dict
from PySide6.QtCore import Slot, Signal, QTimer, QObject
from PySide6.QtGui import QImage
from db.db_cctv_list import DbCctvList, get_cctv_list
from setting import paths
from setting.use_qsetting import Setting
from widget.video_process_pipeline.video_config import VideoConfig, setup_logger, PerformanceData
from widget.video_process_pipeline.video_process_manager import ProcessManager
from widget.video_process_pipeline.frame_receiver import FrameReceiver
from widget.video_process_pipeline.video_player_widget import VideoPlayerWidget
from rich.console import Console
console = Console()


SETTING_DICT: dict =  Setting(paths.GLOBAL_SETTING_PATH).to_dict()
GLOBAL_SETTING: dict = SETTING_DICT.get("global", {})
SYSTEM_CHECK_TIME = int(GLOBAL_SETTING.get("system_check_time", 60))

class BackgroundController(QObject):
    metrics_updated = Signal(dict)

    def __init__(self, cctv_list: List[Dict[str, str]], max_num: int, video_player_widget_list: List[VideoPlayerWidget]):
        super().__init__()
        self.logger = setup_logger("BackgroundController")
        self.output_queue = mp.Queue(maxsize=72)
        self.event_grid_queue = mp.Queue(maxsize=72)
        self.video_config_list = self.get_video_config(cctv_list, max_num)
        self.process_manager = ProcessManager(self.output_queue,self.event_grid_queue)
        self.frame_receiver = FrameReceiver(self.output_queue,self.event_grid_queue)
        self.video_player_widget_list = video_player_widget_list
        self.perf_timer = QTimer()
        self.perf_timer.timeout.connect(self.event_timer)
        self.start_all_processes()

    def get_video_config(self, cctv_list: List[Dict[str, str]], max_num: int) -> List[VideoConfig]:
        """DB에서 camera_list의 모든 정보를 가져와서 VideoConfig 객체로 변환한다"""
        video_config_list = []
        for index, cctv_info in enumerate(cctv_list):
            if max_num != -1 and index >= max_num:
                break
            video_config = VideoConfig()
            video_config.video_number = index
            video_config.device = 0 if index % 2 == 0 else 1 # 백그라운드 프로세스 GPU0, GPU1 분산 할당
            video_config.is_visualize = False
            video_config.event = cctv_info["events"]
            video_config.camera_info = cctv_info["stream_info"]
            video_config_list.append(video_config)
        return video_config_list

    def start_all_processes(self):
        """모든 프로세스를 시작합니다."""
        self.logger.info("프로세스 시작 요청")
        self.connect()
        self.perf_timer.start(SYSTEM_CHECK_TIME * 1000)
        for config in self.video_config_list:
            self.add_new_process(config)

    def stop_all_processes(self):
        """모든 프로세스를 정지합니다."""
        self.logger.info("모든 프로세스 정지 요청")
        # self.frame_receiver.stop()
        # self.disconnect()
        self.perf_timer.stop()
        self.process_manager.stop_all()

    def add_new_process(self, video_config: VideoConfig):
        """새로운 비디오 프로세스를 생성합니다."""
        self.process_manager.create_video_process(video_config)
        time.sleep(0.04)

    def get_video_list(self) -> List[VideoConfig]:
        # console.log(self.video_config_list)
        return self.video_config_list
    
    def connect(self):
        _fr_run_status = self.frame_receiver.isRunning()
        if not _fr_run_status:
            self.frame_receiver.start()
            self.frame_receiver.frame_received.connect(self.on_background_frame_received)
            self.frame_receiver.performance_data_received.connect(self.on_performance_data_received)
            self.frame_receiver.stream_status_received.connect(self.on_stream_status_received)
            self.logger.info(f"프레임 리시버 실행 상태: {_fr_run_status}")
        else:
            self.logger.info("프레임 리시버 실행 중")

    def disconnect(self):
        # try:
        #     while self.output_queue.empty():
        #         self.output_queue.get_nowait()
        # except queue.Empty:
        #     pass
        # finally:
        #     time.sleep(1)
        # self.frame_receiver.frame_received.disconnect(self.on_background_frame_received)
        # self.frame_receiver.stop()
        # _fr_run_status = self.frame_receiver.isRunning()
        # self.logger.info(f"프레임 리시버 실행 상태: {_fr_run_status}")
        pass

    def reconnect_all_streams(self):
        """모든 CCTV 스트림 재연결 시도"""
        self.logger.info("모든 CCTV 스트림 재연결 시도")
        self.process_manager.reconnect_all_streams()

    @Slot(VideoConfig, QImage)
    def on_background_frame_received(self, cctv_info: VideoConfig, q_image: QImage):
        video_number = cctv_info.video_number

        # for video_player_widget in self.video_player_widget_list:
        video_player_widget = self.video_player_widget_list[0]
        if video_player_widget.grid_video_mapping:
            for grid_idx, vid_num in video_player_widget.grid_video_mapping.items():
                if vid_num == video_number and grid_idx in video_player_widget.video_widgets:
                    widget = video_player_widget.video_widgets[grid_idx]
                    if hasattr(widget, 'update_frame'):
                        widget.update_frame(q_image)
                    break

    @Slot(PerformanceData)
    def on_performance_data_received(self, perf_data: PerformanceData):
        """프로세스로부터 성능 데이터를 수신합니다."""
        if not hasattr(self, 'perf_data_dict'):
            self.perf_data_dict = defaultdict(float)
        
        cctv_name = perf_data.cctv_name
        current_frame = perf_data.current_frame
        original_fps = perf_data.original_fps
        client_side_rps = perf_data.client_side_rps
        client_side_frame_rate = perf_data.client_side_frame_rate
        event_dict = perf_data.event_dict

        self.perf_data_dict[cctv_name] = {
            "current_frame": current_frame,
            "original_fps": original_fps,
            "client_side_rps": client_side_rps,
            "client_side_frame_rate": client_side_frame_rate,
            "event_dict": event_dict,
        }
   
    @Slot(dict)
    def on_stream_status_received(self, status_data: dict):
        """스트림 상태 수신 처리"""
        video_number = status_data.get("video_number")
        is_healthy = status_data.get("is_healthy")
        self.process_manager.update_stream_health(video_number, is_healthy)

    @Slot(dict)
    def event_timer(self):
        """타이머 이벤트 핸들러로, 주기적으로 메트릭을 가져오고 출력합니다."""
        if not hasattr(self, 'perf_data_dict'):
            return
        
        if not self.perf_data_dict:
            return
        
        self.get_rps()

    def parse_prometheus_text(self, text_data: str):
        """
        Prometheus 텍스트 형식 데이터를 파싱하여 딕셔너리로 반환합니다.
        {
            'metric_name': [
                {'label1': 'value1', 'value': 123},
                {'label2': 'value2', 'value': 456}
            ]
        }
        """
        metrics = {}
        
        for line in text_data.strip().split('\n'):
            # 주석이거나 빈 줄이면 건너뛰기
            if line.startswith('#') or not line:
                continue
                
            # 메트릭 이름과 값 분리
            parts = line.split()
            value = float(parts[-1])
            metric_part = " ".join(parts[:-1])

            # 메트릭 이름과 레이블 분리
            match = re.match(r'([a-zA-Z_:][a-zA-Z0-9_:]*)({(.*)})?', metric_part)
            if not match:
                continue
                
            metric_name, _, labels_str = match.groups()
            
            record = {}
            if labels_str:
                # 레이블 문자열을 딕셔너리로 변환
                # 예: gpu_uuid="...",model="..." -> {'gpu_uuid': '...', 'model': '...'}
                labels = dict(re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)="([^"]*)"', labels_str))
                record.update(labels)
                
            record['value'] = value
            
            # 최종 결과 딕셔너리에 추가
            if metric_name not in metrics:
                metrics[metric_name] = []
            metrics[metric_name].append(record)
            
        return metrics
    
    def create_metrics(self, metrics: dict):
        """
        파싱된 메트릭 데이터를 CCTV 기준으로 재구성합니다. (자연정렬 적용)
        """
        
        # 1. GPU별 메트릭 데이터 파싱 (기존 코드)
        gpu_metrics = defaultdict(list)
        records = metrics.get("nv_inference_request_success", [])

        if not records:
            self.logger.warning("nv_inference_request_success 메트릭이 없습니다.")
            return

        for record in records:
            gpu_id = record.get("gpu_uuid")
            model_name = record.get("model")
            
            if not all((gpu_id, model_name)) or gpu_id == 'N/A':
                continue

            gpu_metrics[gpu_id].append({
                'model_name': model_name,
                'value': float(record.get("value", 0.0))
            })

        # 2. CCTV 기준으로 데이터 재구성 (임시 딕셔너리)
        cctv_list = get_cctv_list()
        temp_structure = {}
        
        for cctv in cctv_list:
            camera_name = cctv.get("camera_name", "")
            if not camera_name:
                continue
                
            perf_data = self.perf_data_dict.get(camera_name, {})
            current_frame = perf_data.get("current_frame", 0)
            original_fps = perf_data.get("original_fps", 0.0)
            client_frame_rate = perf_data.get("client_side_frame_rate", 0.0)
            event_dict = perf_data.get("event_dict", {})
            model_list = event_dict.get("models", [])

            # CCTV 기본 정보 초기화
            temp_structure[camera_name] = {
                "current_frame": current_frame,
                "original_fps": original_fps,
                "client_side_frame_rate": client_frame_rate,
                "assigned_events": {}
            }

            unsafe_events = cctv.get("unsafe_event", "")
            if unsafe_events is None:
                unsafe_events = ["Unknown"]
            else:
                event_names = [e.strip() for e in unsafe_events.split(',') if e.strip()]

            for event_name in event_names:
                skip_frame = event_dict.get("skip_frame", 1)
                if original_fps > 0.0 and skip_frame > 0:
                    estimated_rps = round(original_fps / skip_frame, 2)
                else:
                    estimated_rps = 0.0

                # AI 모델들 수집 (중복 제거)
                ai_model_names = set()
                for model in model_list:
                    if model.get("type") == "AI":
                        model_name = model.get("name", "")
                        if model_name:
                            ai_model_names.add(model_name)

                # 이벤트별 AI 모델들 정보 구성
                temp_structure[camera_name]["assigned_events"][event_name] = {
                    "ai_models": {}
                }

                # 각 AI 모델별로 GPU 정보 매칭
                for ai_model_name in ai_model_names:
                    gpu_id = None
                    client_side_rps = perf_data.get("client_side_rps", 0.0)
                    
                    # GPU 매칭
                    for gpu, gpu_models in gpu_metrics.items():
                        for gpu_model in gpu_models:
                            if gpu_model["model_name"] == ai_model_name:
                                gpu_id = gpu
                                break
                        if gpu_id:
                            break

                    temp_structure[camera_name]["assigned_events"][event_name]["ai_models"][ai_model_name] = {
                        "gpu_id": gpu_id or "N/A",
                        "skip_frame": skip_frame,
                        "client_side_rps": client_side_rps,
                        "estimated_rps": estimated_rps
                    }

        # 3. 자연정렬 적용
        def natural_sort_key(camera_name):
            return [int(text) if text.isdigit() else text.lower() 
                    for text in re.split('([0-9]+)', camera_name)]
        
        final_structure = {}
        for camera_name in sorted(temp_structure.keys(), key=natural_sort_key):
            final_structure[camera_name] = temp_structure[camera_name]
        
        return final_structure

    def get_rps(self):
        """
        메트릭을 가져와 파싱하고 테이블로 출력하는 전체 워크플로우를 실행합니다.

        예시 출력:
        filtered_metric = {
            'CCTV 1': {                                                                                                                                                                  
                'current_frame': 2711,                                                                                                                                                   
                'original_fps': 30.0,                                                                                                                                                    
                'client_side_frame_rate': 30.1,                                                                                                                                          
                'assigned_events': {                                                                                                                                                     
                    'CCTV1': {'gpu_id': 'GPU-29cee7ba-3d60-4839-8111-11b8d0f37f28', 'skip_frame': 1, 'client_side_rps': 22.6, 'estimated_rps': 30.0}                                     
                }                                                                                                                                                                        
            },                                                                                                                                                                           
            'CCTV 2': {                                                                                                                                                                  
                'current_frame': 2721,                                                                                                                                                   
                'original_fps': 30.0,                                                                                                                                                    
                'client_side_frame_rate': 30.0,                                                                                                                                          
                'assigned_events': {                                                                                                                                                     
                    'CCTV2': {'gpu_id': 'GPU-48fbdb57-39b3-ddf5-f475-22c4f503764d', 'skip_frame': 3, 'client_side_rps': 10.0, 'estimated_rps': 10.0}                                     
                }                                                                                                                                                                        
            }, ...
        """
        metrics_url = 'http://[::1]:8002/metrics'

        try:
            response = requests.get(metrics_url)
            response.raise_for_status()
            
            metrics_text = response.text
            
            # 1. 메트릭 텍스트를 파싱
            parsed_metrics = self.parse_prometheus_text(metrics_text)
            
            # 2. 파싱된 데이터를 rich 테이블로 출력
            metrics = self.create_metrics(parsed_metrics)
            filtered_metric = {
                cctv_name: cctv_data 
                for cctv_name, cctv_data in metrics.items()
                if cctv_data.get('client_side_frame_rate', 0.0) > 0.0
                and cctv_data.get('assigned_events', {})
            }
            self.metrics_updated.emit(filtered_metric)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Metrics 요청 중 오류 발생: {e}")

    # def closeEvent(self, event):
    #     self.logger.info("애플리케이션 종료 요청")
    #     self.stop_all_processes()
    #     event.accept()        