# gpu_worker_process.py
import re
import time
import datetime
import queue
import requests
import threading
import multiprocessing as mp
import gc
import cv2
import torch
import numpy as np
from pathlib import Path
from collections import deque, defaultdict
from typing import Dict, List, Optional, DefaultDict, Set
from ultralytics import YOLO
from ultralytics.engine.results import Results, Annotator, colors, Boxes
from PySide6.QtCore import QTime, QTimer, QDateTime
from rich.console import Console
from tritonclient.utils import InferenceServerException
from setting import paths
from setting.use_qsetting import Setting
from event_logic.event_logic_func import EventLogic
from event_logic.setup_event_logic import SetupEventLogic
from widget.video_process_pipeline.video_config import setup_logger, ConfigManager, VideoConfig, FrameData, EventLogData, DisplayGridData, EventGridData, PerformanceData, \
                                                MessageType, JigukSessionData, DangerType, RiskLevel, FrameStatus, ColorType, RiskLevel_1
from widget.video_process_pipeline.video_writer import VideoWriter


"""
영상처리 프로세스 파이프라인 구조
run
  ├── initialize_gpu_resources
  ├── video_thread → _video_reading_loop
  │                    ├── _preprocess_for_detection → detection_queue
  │                    └── _send_frame_to_gui → _draw_detections → output_queue
  └── detector_thread → _detection_loop → latest_detections

_video_reading_loop : video_thread에서 GPU로 프레임을 읽고 전처리 후 detection_queue에 전달.
_detection_loop     : detector_thread에서 큐의 프레임을 처리해 감지 결과를 저장.
_draw_detections    : 시각화가 활성화되면 프레임에 감지 결과를 그리고 GUI로 전송.
self.command_queue  : run 루프에서 외부 명령을 처리하며 종료 시 cleanup 호출.
"""

console = Console()
PROJECT_ROOT: str = paths.PROJECT_ROOT
INI_CONFIG = ConfigManager()

class VideoProcess:
    def __init__(self, config: VideoConfig, command_queue: mp.Queue, output_queue: mp.Queue, event_grid_queue: mp.Queue):
        self.config: VideoConfig = config
        self.command_queue: Dict[queue.Queue] = command_queue
        self.output_queue: queue.Queue = output_queue
        self.event_grid_queue: queue.Queue = event_grid_queue
        self.logger = setup_logger(f"Video{config.video_number}")
        
        font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        self.ft = cv2.freetype.createFreeType2()
        self.ft.loadFontData(font_path, 0)

        self.is_running: bool = False
        self.is_visualizing: bool = config.is_visualize
        self.is_danger: bool = False
        self.danger_timer: threading.Timer = None
        self.frame_counter: int = 0
        self.consecutive_frame_failures = 0
        self.last_successful_frame_time = time.time()

        self.gpu_reader: cv2.cudacodec.VideoReader = None
    
        # 이벤트 스레드용 변수 -> 공유되면 안됨
        self.model: List[YOLO] = []
        self.models: DefaultDict[int, Dict[str, YOLO]] = defaultdict(dict) # 이벤트별 모델 보관: event_index -> { model_name -> YOLO }
        self.classes_by_event: DefaultDict[int, DefaultDict[str, Set[int]]] = defaultdict(lambda: defaultdict(set)) # 이벤트별 사용 클래스 집합: event_index -> { model_name -> {class_index, ...} }
        self.latest_detections: List = []
        self.prev_result: Results = None
        self.roi: List[np.ndarray] = []

        self.frame_bgr: np.ndarray = None
        self.frame_buffer: deque = deque(maxlen=INI_CONFIG.global_config.max_record_buffer_size)  # 최대 150프레임 버퍼 (5초 기준)
        self.frame_buffer_lock: threading.Lock = threading.Lock()
        self.video_thread: threading.Thread = None
        self.detector_thread_list: List[threading.Thread] = []

        self.event_index_list: list[int] = []
        self.event_logic = SetupEventLogic(command_queue)
        self.event_logic_func = EventLogic(None)
        self.filter_dict: Dict[str, Set[int]] = {}

        self.max_retry: int = INI_CONFIG.global_config.max_retry

        # Triton 모델 검증용 딕셔너리
        url = "http://[::1]:8000/v2/repository/index"
        response = requests.post(url, timeout=5)  # 5초 타임아웃
        self.triton_model_list = response.json()
        # self.logger.info(f"Triton 모델 딕셔너리 로드 완료: {self.triton_model_list}")

        self.jiguk_session: JigukSessionData = None
        self.is_jiguk_activate = False
        self.current_algorithm: Dict[int, str] = {}

        self.tracking_id_reset_timer: threading.Timer = None
        self.person_count: int = -1

        self.bulti_roi_timer = None
        self.bulti_roi_last_update_time = 0
        
        self.algorithm_configs: dict[str, dict] = {
            "지적확인": {
                "danger_maintain_time": INI_CONFIG.global_config.jiguk_danger_maintain_time
            },
            "불티비산": {
                "extend_pixel": INI_CONFIG.bulti_config.roi_extend_pixel,
                "roi_trigger_classes": ["bulti"],
                "extra_classes": {"smoke": (0, 0, 255)},
                "danger_maintain_time": INI_CONFIG.global_config.bulti_danger_maintain_time
            },
            "접근감지": {
                "extend_pixel": INI_CONFIG.collision_config.roi_extend_pixel,
                "roi_trigger_classes": ["forklift", "lift"],
                "extra_classes": {},
                "danger_maintain_time": INI_CONFIG.global_config.collision_danger_maintain_time
            },
            "보호구감지": {
                "extend_pixel": INI_CONFIG.flash_suit_config.roi_extend_pixel,
                "roi_trigger_classes": ["flash_fire"],
                "extra_classes": {}
            }
        }

    # 초기화
    def initialize_gpu_resources(self):
        try:
            cv2.cuda.setDevice(self.config.device)
            torch.cuda.set_device(self.config.device)
            
            # 이벤트 설정 로드
            self.create_event_model_context()
            self.init_gpu_reader()
            
            # 자정 타이머 시작
            self._schedule_next_reset()

        except cv2.error as e:
            self.logger.error(f"OpenCV GPU 초기화 실패: {e}")
            raise
        except Exception as e:
            self.logger.error(f"GPU 리소스 초기화 실패: {e}")
            raise

    def create_event_model_context(self):
        """
        이벤트 예시
        {
            "event": [
                {
                    "input_img_size": "640,640",
                    "models": [
                    {
                        "class_index": 0,
                        "class_name": "person",
                        "name": "yolov8x_1",
                        "type": "AI"
                    },
                    {
                        "class_index": 32,
                        "class_name": "sports ball",
                        "name": "yolov8x_1",
                        "type": "AI"
                    },
                    {
                        "class_index": None,
                        "class_name": None,
                        "name": "거리",
                        "type": "algorithm"
                    }
                    ],
                    "name": "사람과 공",
                    "risk_level": 1,
                    "skip_frame": 0
                }
            ]
        }
        """
        if not self.config.event:
            return
        
        for event_index, event in enumerate(self.config.event):
            for model in event["models"]:
                model: dict
                if model.get("type") != "AI":
                    continue

                model_name = model.get("name")

                if not model_name:
                    continue

                if not any(triton_model["name"] == model_name for triton_model in self.triton_model_list):
                    continue

                # 이벤트마다 새로운 YOLO 객체 생성 (공유 금지)
                self.models[event_index][model_name] = YOLO(
                    f"grpc://[::1]:8001/{model_name}", task="detect", verbose=False
                )

                # 이벤트별로 사용할 클래스 인덱스 집계
                class_index = model.get("class_index")
                if class_index is not None:
                    self.classes_by_event[event_index][model_name].add(class_index)

    def init_gpu_reader(self):
        """
        GPU 비디오 리더 초기화
        """
        params = cv2.cudacodec.VideoReaderInitParams()
        params.udpSource = True
        params.allowFrameDrop = True
        
        self.gpu_reader = cv2.cudacodec.createVideoReader(self.config.camera_info["stream_url"], params=params)
        # self.logger.info(f"GPU{self.config.device} 리소스 초기화 완료 - Video {self.config.video_number}")

    # 메인 함수
    def run(self):
        """프로세스 메인 루프"""
        try:
            self.initialize_gpu_resources()
            self.is_running = True

            cctv_location = self.config.camera_info["camera_location"]
            cctv_name = self.config.camera_info["camera_name"]
            event_name = self.config.event[0]["name"] if self.config.event else "Uknown Event"
            # 이벤트 위험도 매핑 실패: list index out of range, Unknown으로 초기화
            try:
                risk_level: RiskLevel_1 = RiskLevel_1(self.config.event[0]["risk_level"])
                severity = risk_level.name
            except Exception as e:
                #초기화 시 self.config.event 미존재로 인한 오류 발생 -> Unknown 예외처리
                self.logger.info(f"[{cctv_name}] 이벤트 위험도 매핑 실패: {e}, Unknown으로 초기화")
                severity = "Unknown"

            event_risk_level = self.config.event[0]["risk_level"] if self.config.event else -1
            image_path = ""

            self.event_log = EventLogData(
                cctv_location=cctv_location,
                cctv_name=cctv_name,
                event_name=event_name,
                event_risk_level=event_risk_level,
                image_path=image_path,
                severity=severity,
            )

            self.video_thread = threading.Thread(target=self._video_reading_loop, daemon=True, name=f"{cctv_name} VideoThread")
            self.video_thread.start()

            if self.config.event:
                for event_index, event in enumerate(self.config.event):
                    camera_name = self.config.camera_info["camera_name"]
                    detector_thread_name = f"[{camera_name}] Detector-{event['name']}"
                    detector_thread = threading.Thread(target=self._detection_loop, daemon=True, name=detector_thread_name, args=(event_index,))
                    self.detector_thread_list.append(detector_thread)
                    detector_thread.start()
            else:
                # 이벤트가 없는 경우 감지 스레드 실행 안함
                pass

            self.event_logic.set_config(self.config)

            # 프로세스 간 커맨드 입력
            while self.is_running:
                try:
                    message = self.command_queue.get(timeout=0.1)
                    
                    if message['type'] == MessageType.RECONNECT:
                        self.logger.info("스트림 재연결 명령 수신")
                        try:
                            if self.gpu_reader:
                                del self.gpu_reader
                                self.gpu_reader = None
                            
                            time.sleep(1)
                            self.init_gpu_reader()
                            self.logger.info("스트림 재연결 성공")
                        except Exception as e:
                            self.logger.error(f"스트림 재연결 실패: {e}")

                    # 시각화 토글
                    if message['type'] == MessageType.UPDATE_VISUALIZATION:
                        self.is_visualizing = message['is_visualize']
                        # self.logger.info(f"시각화 상태 변경: {self.is_visualizing}")
                    
                    # 끌 때
                    elif message['type'] == MessageType.SHUTDOWN:
                        # self.logger.info("종료 명령 수신")
                        self.is_running = False
                        break

                    if message['type'] == MessageType.RECORD:
                        jiguk_record_thread = threading.Thread(target=self._jiguk_record_loop, daemon=True, name=f"{cctv_name} JigukRecordThread_{time.time()}", args=(message,))
                        jiguk_record_thread.start()

                except cv2.error as e:
                    self.logger.error(f"OpenCV 오류: {e}")

                except queue.Empty:
                    continue

                except Exception as e:
                    self.logger.error(f"명령 처리 오류: {e}")

        except Exception as e:
            self.logger.error(f"메인 루프 초기화 오류: {e}")

        finally:
            self.cleanup()

    #region 스레드
    def _video_reading_loop(self):
        """비디오 읽기 루프 - 별도 스레드에서 실행"""
        cv2.cuda.setDevice(self.config.device)
        torch.cuda.set_device(self.config.device)

        _, float_fps = self.gpu_reader.get(cv2.CAP_PROP_FPS)
        self.config.cctv_fps = float_fps
        retry_counter = 0
        reconnect_counter = 0
        max_reconnect_attempts = 1000

        gpu_frame = None
        frame_bgr = None
        self._send_stream_status(is_healthy=True)
        
        while self.is_running:
            try:
                # GPU reader가 None인 경우 처리
                if self.gpu_reader is None:
                    if reconnect_counter >= max_reconnect_attempts:
                        self.logger.error("최대 재연결 횟수 초과, 스레드 종료")
                        self._send_stream_status(is_healthy=False)
                        self.is_running = False
                        break
                    
                    self.logger.warning(f"GPU reader 재연결 시도 ({reconnect_counter + 1}/{max_reconnect_attempts})")
                    try:
                        time.sleep(2)
                        self.init_gpu_reader()
                        _, float_fps = self.gpu_reader.get(cv2.CAP_PROP_FPS)
                        self.config.cctv_fps = float_fps
                        self.logger.info("GPU reader 재연결 성공")
                        retry_counter = 0
                        reconnect_counter += 1
                        continue
                    except Exception as e:
                        self.logger.error(f"GPU reader 재연결 실패: {e}")
                        self.gpu_reader = None
                        reconnect_counter += 1
                        time.sleep(10)
                        continue

                ret, gpu_frame = self.gpu_reader.nextFrame()
                if not ret:
                    self.consecutive_frame_failures += 1
                    self.logger.warning("프레임 읽기 실패, 재시도...")

                    # 연속 실패 횟수가 임계값을 초과하면 스트림 비정상 상태 전송
                    if self.consecutive_frame_failures >= self.max_retry:
                        self._send_stream_status(is_healthy=False)

                    if retry_counter >= self.max_retry:
                        # 최대 재시도 횟수 초과 시 GPU reader 재초기화 시도
                        self.logger.warning(f"최대 재시도 횟수 초과, GPU reader 재연결 준비")
                        
                        # 기존 GPU reader 정리
                        if self.gpu_reader:
                            try:
                                del self.gpu_reader
                            except:
                                pass
                            self.gpu_reader = None
                        
                        retry_counter = 0
                        continue
                    else:
                        retry_counter += 1
                        time.sleep(1)
                        continue
                else:
                    # 프레임 읽기 성공 시 카운터 리셋
                    retry_counter = 0
                    reconnect_counter = 0  # 성공 시 재연결 카운터도 리셋
                    
                    # 연속 실패 후 다시 정상 동작 시 상태 전송
                    if self.consecutive_frame_failures >= self.max_retry:
                        self._send_stream_status(is_healthy=True)
                    
                    self.consecutive_frame_failures = 0
                    self.last_successful_frame_time = time.time()

                # 프레임 큐에 저장
                self._store_frame_in_deque(gpu_frame.clone())

                self.frame_bgr = self._convert_gpu_frame_to_cpu_frame(gpu_frame)

                # 시각화가 활성화된 경우 프레임 전송
                if self.is_visualizing:
                    frame_bgr = self._send_frame_to_gui()
                else:
                    frame_bgr = self.frame_bgr

                # 비디오 저장 중인 경우 프레임 추가
                if hasattr(self, 'video_writer'):
                    self.video_writer: VideoWriter
                    if self.video_writer:
                        if self.video_writer.is_recording:
                            self.video_writer.add_frame(frame_bgr)
                
            except AttributeError as e:
                if "'NoneType' object has no attribute 'nextFrame'" in str(e):
                    self.logger.warning("GPU reader가 None 상태, 재연결 시도")
                    self.gpu_reader = None
                    self._send_stream_status(is_healthy=False)
                    continue
                else:
                    raise
                    
            except Exception as e:
                self.logger.error(f"비디오 읽기 루프 오류: {e}")
                self._send_stream_status(is_healthy=False)
                time.sleep(1)
                continue

            finally:
                # FPS 제어
                multiply = 15
                if self.config.cctv_fps > 40:
                    multiply *= 2
                time.sleep(1 / (self.config.cctv_fps + multiply))
                self.frame_counter += 1
                try:
                    del gpu_frame
                except (NameError, UnboundLocalError):
                    pass
                
                try:
                    del frame_bgr
                except (NameError, UnboundLocalError):
                    pass
    
    def _detection_loop(self, event_index: int):
        """
        객체 감지 루프 - 별도 스레드에서 실행
        이벤트의 개수에 따라 복수의 스레드가 실행 될 수 있음

        event: [
            {
            'input_img_size': '640,640',
            'models': [
                {
                'class_index': 0,
                'class_name': 'person',
                'name': 'yolov8x_1',
                'type': 'AI'
                },
                {
                'class_index': 32,
                'class_name': 'sports ball',
                'name': 'yolov8x_1',
                'type': 'AI'
                },
                {
                'class_index': None,
                'class_name': None,
                'name': '거리',
                'type': 'algorithm'
                }
            ],
            'name': '사람과 공',
            'risk_level': 1,
            'skip_frame': 0
            }
        ]
        """
        cv2.cuda.setDevice(self.config.device)
        torch.cuda.set_device(self.config.device)
        
        # 1) 이벤트별 모델 딕셔너리 꺼내기: { model_name: YOLO }
        event_models: dict[str, YOLO] = self.models.get(event_index, {})
        self._set_current_algorithm(event_index)

        # 2) 최소 처리 프레임 설정
        event_data: dict = self.config.event[event_index]
        skip_frame: int = max(event_data.get("skip_frame", INI_CONFIG.global_config.min_skip_frame), INI_CONFIG.global_config.min_skip_frame)

        # 3) 클래스 필터 정보: { model_name: {class_index, ...} }
        class_filters: dict[str, set[int]] = {
            mn: set(ci_set)
            for mn, ci_set in self.classes_by_event.get(event_index, {}).items()
        }
        self.filter_dict = class_filters

        # 성능 계산용
        request_count: int = 0
        start_time: float = time.time()
        cctv_name: str = self.config.camera_info["camera_name"]
        estimate_time: float = 10.0
        prev_frame_count: int = 0

        # 4) 루프
        while self.is_running:
            try:
                current_time = time.time()
                current_frame = self.frame_counter

                if self.frame_counter % skip_frame == 0 and self.frame_counter > 0 and self.frame_bgr is not None:
                    # 모델별 추론 수행 -> { model_name: results[0] }
                    request_count += 1
                    results_by_model = self._predict(self.config, self.frame_bgr, event_models)

                    if time.time() - start_time >= estimate_time:
                        client_side_rps = round(request_count / estimate_time, 2)
                        client_side_frame_rate = round((current_frame - prev_frame_count) / estimate_time, 2)
                        perf_data = PerformanceData(
                            cctv_name=cctv_name,
                            current_frame=current_frame,
                            original_fps=self.config.cctv_fps,
                            client_side_rps=client_side_rps,
                            client_side_frame_rate=client_side_frame_rate,
                            event_dict=self.config.event[event_index]
                        )
                        self._safe_put_queue(self.output_queue, perf_data)

                        start_time = time.time()
                        request_count = 0
                        prev_frame_count = current_frame

                    # 필터/로직 적용 -> self.latest_detections 업데이트
                    detections = self._create_danger_detection(results_by_model, class_filters)

                    if event_index == 0:
                        first_model_name = next(iter(event_models))
                        self.prev_result = results_by_model[first_model_name]
                        self.latest_detections = detections

                    # 위험 판단 및 후속 처리
                    if self._check_ai_detection_result_by_dynamic_event_process(event_index, detections):

                        danger_maintain_time = INI_CONFIG.global_config.danger_maintain_time
                        if self.latest_detections:
                            for algorithm_name in self.algorithm_configs.keys():
                                if self.current_algorithm[event_index] == algorithm_name:
                                    danger_maintain_time = self.algorithm_configs[algorithm_name]["danger_maintain_time"]
                                    break
                        self._handle_danger_detection(event_index, DangerType.OTHER_DANGER, current_time, danger_maintain_time)

            except InferenceServerException:
                pass

            multiply = 15
            if self.config.cctv_fps > 40:
                multiply *= 2
            time.sleep(1 / (self.config.cctv_fps + multiply))

    def _jiguk_record_loop(self, message: dict):
        """
        JigukSessionData(
            event_index=0,
            session_id='CCTV 1_13_20250729_130917',
            start_time=1753762157.1250784,
            end_time=1753765157.1250784,
            jiguk_check_deque=deque([True, True, True, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], maxlen=30),
            jiguk_performed=True,
            consecutive_no_intersection=2,
            jiguk_direction='RIGHT',
            direction_result_str='오른쪽으로 이동',
            initial_center=(39.5, 399.0),
            final_center=(196.5, 356.0)
        )

        """
        current_cctv_name = self.event_log.cctv_name
        status_label_for_record_video_file_name = message.get("status_label", "")
        session: JigukSessionData = message.get("session", JigukSessionData())
        self.jiguk_session = session
        try:
            # 패턴: "_id_" 다음에 오는 숫자 추출
            match = re.search(r"_id_(\d+)", session.session_id)
            tracked_id = int(match.group(1)) if match else -1
        except (AttributeError, ValueError, IndexError) as e:
            tracked_id = -1
            self.logger.warning(f"Session ID에서 tracked_id 추출 실패: {session.session_id}, 오류: {e}")

        event_index: int = session.event_index
        is_record_video = False
        yolo_result: Results = message.get("yolo_result", None)
        
        # 지적확인 위험상황 처리
        if session.jiguk_performed:
            self._jiguk_activate(event_index)

        if not session.jiguk_performed:
            danger_type = DangerType.JIGUK_DANGER
            self._handle_danger_detection(event_index, danger_type, session.end_time, INI_CONFIG.global_config.jiguk_danger_maintain_time)

        def save_image_async():
            if yolo_result is None:
                return
            
            _, _, image_path = self._get_file_path_info("img", "jpg")
            image_path = Path(image_path).stem

            current_date = time.strftime("%Y-%m-%d", time.localtime(session.end_time))
            current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(session.end_time))
            subfolder = "img"
            extension = "jpg"

            target_path = Path(f"{PROJECT_ROOT}/{subfolder}/{current_date}")
            target_path.mkdir(parents=True, exist_ok=True)
            
            file_path = target_path / f"{current_time}_{current_cctv_name}_Track_ID_{tracked_id}_{status_label_for_record_video_file_name}.{extension}"

            frame_bgr = yolo_result.plot(line_width=INI_CONFIG.global_config.line_width, labels=False)
            frame_bgr_cropped = self._scale_frame_to_letterbox(frame_bgr)

            # 지적확인 여부 GUI 표시
            annotated_img = self._process_danger_frame(frame_bgr_cropped)

            cv2.imwrite(str(file_path), annotated_img, [cv2.IMWRITE_JPEG_QUALITY, 75])  # Path를 str로 변환

            self.event_log.image_path = str(file_path)
            self.event_log.timestamp = session.end_time
            self.event_log.cctv_location = self.event_log.cctv_location
            self.event_log.cctv_name = self.event_log.cctv_name
            self.event_log.event_name = self.config.event[0]["name"]
            
            if self.jiguk_session.jiguk_performed:
                RISK_LEVEL = RiskLevel_1.good_mid
            else:
                RISK_LEVEL = RiskLevel_1.danger_mid

            # EventLogData의 severity 업데이트 추가
            self.event_log.severity = RiskLevel_1(RISK_LEVEL).name

            max_retries = 5
            retry_delay = 0.1  # 100ms

            for attempt in range(max_retries):
                try:
                    event_frame_data = FrameData(
                        cctv_info=self.config,
                        event_log=self.event_log,
                        frame=None,
                        detections=[],
                        is_event_notification=True,
                        severity=self.event_log.severity,
                    )
                    
                    if attempt == 0:
                        self.output_queue.put_nowait(event_frame_data)
                    else:
                        timeout = retry_delay * (attempt + 1)
                        self.output_queue.put(event_frame_data, timeout=timeout)
                    break

                except queue.Full:
                    if attempt < max_retries - 1:
                        try:
                            removed_count = 0
                            temp_items = []
                            
                            while not self.output_queue.empty() and removed_count < 3:
                                try:
                                    item = self.output_queue.get_nowait()
                                    if not getattr(item, 'is_event_notification', False):
                                        removed_count += 1
                                    else:
                                        temp_items.append(item)
                                except queue.Empty:
                                    break
                            
                            for item in temp_items:
                                try:
                                    self.output_queue.put_nowait(item)
                                except queue.Full:
                                    break
                            
                        except Exception as e:
                            self.logger.warning(f"큐 정리 중 오류: {e}")
                        
                        time.sleep(retry_delay * (attempt + 1))
                    else:
                        self.logger.error(f"이벤트 로그 전송 실패 - 최대 재시도 횟수 초과: {self.event_log.event_name}")
                        
                except Exception as e:
                    self.logger.error(f"이벤트 로그 전송 오류 (시도 {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))
                    else:
                        break

        def save_video_async():
            try:
                # self.logger.info(f"지적확인 정보 조회: {status_label_for_record_video_file_name}")

                # if status_label_for_record_video_file_name == "지적확인_실시":
                #     return
            
                # self.logger.info(f"지적확인 버퍼 체크")
                if len(self.frame_buffer) < INI_CONFIG.global_config.max_record_buffer_size:
                    # self.logger.warning(f"[{current_cctv_name}] 프레임 버퍼가 가득 차지 않음 ({len(self.frame_buffer)}/{MAX_RECORD_BUFFER_SIZE}) - 녹화를 시작할 수 없습니다")
                    return

                record_time = time.localtime(session.start_time)
                current_date = time.strftime("%Y-%m-%d", record_time)
                current_time = time.strftime("%Y%m%d_%H%M%S", record_time)
                target_path = paths.VIDEO_OUTPUT_DIR / current_date
                target_path.mkdir(parents=True, exist_ok=True)
                file_path = target_path / f"{current_time}_{current_cctv_name}_{status_label_for_record_video_file_name}.mp4"

                frame_h, frame_w = self.frame_buffer[0].shape[:2]

                video_writer = cv2.VideoWriter(
                    str(file_path),
                    cv2.VideoWriter.fourcc(*"avc1"),
                    self.config.cctv_fps,
                    (frame_w, frame_h)
                )
                
                if not video_writer.isOpened():
                    # self.logger.error(f"[{current_cctv_name}] 비디오 라이터 초기화 실패")
                    return
                    
                # 버퍼가 가득 찬 경우에만 모든 프레임 저장
                # self.logger.info(f"[{current_cctv_name}] 비디오 녹화 시작 - {MAX_RECORD_BUFFER_SIZE} 프레임")

                for i in range(INI_CONFIG.global_config.max_record_buffer_size):
                    video_writer.write(self.frame_buffer[i])
                    
                video_writer.release()
                # self.logger.info(f"[{current_cctv_name}] 비디오 저장 완료: {file_path}")
                
            except Exception as e:
                # self.logger.error(f"[{current_cctv_name}] 비디오 녹화 중 오류: {e}")
                pass
            finally:
                pass

        # 스틸컷 저장
        if not is_record_video:
            internal_thread = threading.Thread(target=save_image_async, name=f"{current_cctv_name}_JigukImageSaveThread_{time.time()}")
        else:
            internal_thread = threading.Thread(target=save_video_async, name=f"{current_cctv_name}_JigukVideoSaveThread_{time.time()}")

        if internal_thread:
            internal_thread.start()

    def _jiguk_activate(self, event_index):
        self.is_jiguk_activate = True
        is_jiguk_activate = self.is_jiguk_activate
        threading.Timer(INI_CONFIG.global_config.jiguk_danger_maintain_time, self._jiguk_deactivate).start()

        event_name = self.config.event[0]['name']
        self._send_danger_notification(event_index=event_index, event_name=event_name, danger_type=DangerType.JIGUK_DANGER, is_jiguk_performed=is_jiguk_activate)

    def _jiguk_deactivate(self):
        self.is_jiguk_activate = False
    #endregion

    #region UI 관련 함수
    def _send_frame_to_gui(self):
        """
        프레임을 GUI로 전송
        _video_reading_loop -> detection_queue -> _detection_loop -> self.latest_detections 갱신 
        _video_reading_loop -> _send_frame_to_gui -> self.output_queue -> FrameReceiver -> video_player_widget.on_frame_received -> video_display_widget.update_frame
        일정주기마다 갱신되는 self.latest_detections를 기반으로 프레임에 감지 결과 삽입

        GPU -> CPU로 이동 된 frame 데이터를 copy하여 frame_bgr에 저장
        frame_bgr은 _video_reading_loop로 반환된 후 해당 함수의 finally에서 정리
        """
        if not self.is_visualizing:
            return
        
        frame_bgr = self.frame_bgr.copy()
        frame_bgr_cropped = None

        try:
            # 감지 결과 시각화
            if self.prev_result:
                frame_bgr = self._custom_plot(frame_bgr)

            # 이벤트별 추가 시각화 ex) ROI 확장
            first_event_algorithm = self.current_algorithm.get(0, "")
            if first_event_algorithm in self.algorithm_configs.keys():
                frame_bgr = self._extend_bbox_visualization(frame_bgr)

            # 프레임 크기 조정 및 레터박싱
            frame_bgr_cropped = self._scale_frame_to_letterbox(frame_bgr)

            # 위험상황 시각화
            if self.is_danger or self.is_jiguk_activate:
                frame_bgr_cropped = self._process_danger_frame(frame_bgr=frame_bgr_cropped, draw_border=True)
            
            # CCTV 명칭 삽입
            frame_bgr_cropped = self._draw_cctv_name_on_frame(frame_bgr_cropped)

            # 작업자 카운터 삽입 (옵션)
            frame_bgr_cropped = self._draw_person_counter_on_frame(frame_bgr_cropped)

            # BGR에서 RGB로 변환 (GUI 전송용)
            frame_rgb = cv2.cvtColor(frame_bgr_cropped, cv2.COLOR_BGR2RGB)

            # 프레임 데이터 생성
            frame_data = FrameData(
                cctv_info=self.config,
                event_log=self.event_log,
                frame=frame_rgb,
                detections=self.latest_detections.copy(),
                severity=getattr(self.event_log, 'severity', ''),
            )
            # GUI로 전송 (non-blocking)
            self.output_queue.put_nowait(frame_data)
            
        except queue.Full:
            self.output_queue.get_nowait()
            self.output_queue.put_nowait(frame_data)
        
        # except Exception as e:
        #     self.logger.error(f"프레임 전송 오류: {e}")
        
        finally:
            if frame_bgr is None:
                return frame_bgr
            return frame_bgr_cropped

    def _custom_plot(self, frame_bgr: np.ndarray, conf: bool = True, line_width: int = INI_CONFIG.global_config.line_width,
                     font_size: Optional[int] = None, labels: bool = True, boxes: bool = True) -> np.ndarray:
        """
        Ultralytics 스타일 시각화 (무거움)

        2025-08-13 수정
        레이블 생성부에서 label = None으로 하면 bbox만 화면에 시각화 됨
        """
        if not self.prev_result:
            return frame_bgr
        
        # Ultralytics Annotator 사용
        annotator = Annotator(
            frame_bgr,
            line_width=line_width,
            font_size=font_size,
            example=self.prev_result.names
        )
        
        if self.prev_result.boxes is not None and boxes:
            for i, box in enumerate(self.prev_result.boxes):
                box : Boxes = box
                if box.is_track:
                    track_ids = int(box.id)
                cls = int(box.cls)
                confidence = float(box.conf) if conf else None
                class_name = self.prev_result.names[cls]


                # if labels and not box.is_track:
                #     label = f"{class_name} {confidence:.2f}" if conf and confidence else class_name
                # elif labels and box.is_track:
                #     label = f"id:{track_ids} {class_name} {confidence:.2f}" if conf and confidence else class_name
                # else:
                #     label = None

                label = None
                bbox = box.xyxy[0].cpu().numpy()
                annotator.box_label(bbox, label, color=colors(cls, True))

        return annotator.result()

    def _extend_bbox_visualization(self, frame_bgr: np.ndarray) -> np.ndarray:
        """
        알고리즘 설정에 따라 감지된 객체 주변의 ROI를 확장하고 시각화합니다.
        - '불티비산' 알고리즘의 경우, ROI가 트리거된 후 객체가 사라져도 ROI가 유지됩니다.
        """
        plot_frame = frame_bgr.copy()
        algorithm_name = self.current_algorithm.get(0)

        if not algorithm_name or algorithm_name not in self.algorithm_configs:
            # 현재 ROI 리스트가 있다면 시각화는 유지 (불티비산 대응)
            if self.roi:
                for roi in self.roi:
                    x1, y1, x2, y2 = map(int, roi)
                    cv2.rectangle(plot_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            return plot_frame

        config: dict = self.algorithm_configs[algorithm_name]
        extend_pixel: int = config["extend_pixel"]
        
        # --- 1. 클래스 이름과 ID 매핑 ---
        class_name_to_id: Dict[str, int] = {
            model.get("class_name"): model.get("class_index")
            for model in self.config.event[0].get("models", [])
            if model.get("class_name") and model.get("class_index") is not None
        }

        roi_trigger_class_names: list[str] = config["roi_trigger_classes"]
        if algorithm_name == "접근감지":
            etc_classes = [
                name for name in class_name_to_id 
                if name not in ["worker", "person"] + roi_trigger_class_names
            ]
            roi_trigger_class_names.extend(etc_classes)

        roi_trigger_ids = {class_name_to_id.get(name) for name in roi_trigger_class_names}
        roi_trigger_ids.discard(None)

        # --- 2. ROI 업데이트 로직 (여러 객체 처리) ---
        new_roi_list = []
        if self.latest_detections:
            for det in self.latest_detections:
                if det["class_id"] in roi_trigger_ids:
                    x1, y1, x2, y2 = det["bbox"]
                    h, w, _ = frame_bgr.shape
                    
                    ex1 = max(0, x1 - extend_pixel)
                    ey1 = max(0, y1 - extend_pixel)
                    ex2 = min(w, x2 + extend_pixel)
                    ey2 = min(h, y2 + extend_pixel)
                    
                    # 각 객체에 대한 ROI를 리스트에 추가
                    new_roi_list.append(np.array([ex1, ey1, ex2, ey2]))

        # --- 3. 조건부 ROI 업데이트 ---
        if algorithm_name == "불티비산":
            current_time = time.time()
            bulti_timeout = INI_CONFIG.bulti_config.roi_maintain_time  # bulti ROI 유지 시간 (초)
            
            # 새로운 ROI가 감지되면 타이머 갱신
            if new_roi_list:
                self.roi = new_roi_list
                self.bulti_roi_last_update_time = current_time
                
                # 기존 타이머 취소
                if self.bulti_roi_timer:
                    self.bulti_roi_timer.cancel()
                
                # 새 타이머 시작
                self.bulti_roi_timer = threading.Timer(
                    bulti_timeout,
                    self._clear_bulti_roi
                )
                self.bulti_roi_timer.daemon = True
                self.bulti_roi_timer.start()
            else:
                # 새 ROI가 없지만 타이머가 만료되지 않았으면 기존 ROI 유지
                elapsed_time = current_time - self.bulti_roi_last_update_time
                if elapsed_time >= bulti_timeout:
                    self.roi = []
                # else: self.roi 유지 (기존 ROI가 계속 표시됨)
        else:
            # 불티비산이 아닌 경우
            if new_roi_list:
                self.roi = new_roi_list
            else:
                self.roi = []

        # --- 4. ROI 시각화 (모든 ROI 표시) ---
        if self.roi:
            for roi in self.roi:
                x1, y1, x2, y2 = map(int, roi)
                cv2.rectangle(plot_frame, (x1, y1), (x2, y2), (0, 255, 0), INI_CONFIG.global_config.line_width)

        # --- 5. 추가 객체 시각화 ---
        extra_draw_ids = {
            class_name_to_id.get(name): color 
            for name, color in config["extra_classes"].items()
        }
        extra_draw_ids.pop(None, None)

        if self.latest_detections and extra_draw_ids:
            for det in self.latest_detections:
                if det["class_id"] in extra_draw_ids:
                    color = extra_draw_ids[det["class_id"]]
                    x1, y1, x2, y2 = det["bbox"]
                    cv2.rectangle(plot_frame, (x1, y1), (x2, y2), color, INI_CONFIG.global_config.line_width)
                    
        return plot_frame

    def _process_danger_frame(self, frame_bgr: np.ndarray, draw_border: bool = False, circle_mode: bool = INI_CONFIG.global_config.danger_indicator_circle_mode) -> np.ndarray:
        # 1. 위험 레벨에 따른 텍스트, 색상 결정
        first_event_dict: dict = self.config.event[0]
        risk_level: int = int(first_event_dict.get("risk_level", 0))
        if self.jiguk_session:
            if self.jiguk_session.jiguk_performed:
                RISK_LEVEL = RiskLevel.GOOD
            else:
                RISK_LEVEL = RiskLevel.BAD
        else:
            if risk_level < 2:
                RISK_LEVEL = RiskLevel.CAUTION
            else:
                RISK_LEVEL = RiskLevel.WARNING
        DEFAULT_STATUS = FrameStatus("DANGER", ColorType.RED)
        RISK_STATUS_MAP = {
            RiskLevel.WARNING: FrameStatus("WARNING", ColorType.RED),
            RiskLevel.CAUTION: FrameStatus("CAUTION", ColorType.YELLOW),
            RiskLevel.BAD: FrameStatus("BAD", ColorType.RED),
            RiskLevel.GOOD: FrameStatus("GOOD", ColorType.YELLOW)
        }

        STATUS: FrameStatus = RISK_STATUS_MAP.get(RISK_LEVEL, DEFAULT_STATUS)
        text = STATUS.text
        frame_color = STATUS.color.value

        # 2. 프레임 크기 및 텍스트 위치 계산
        danger_frame = frame_bgr
        _, w = danger_frame.shape[:2]

        rect_w, rect_h = 150, 50
        rect_start_point = (w - rect_w, 0)
        rect_end_point = (w, rect_h)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        font_thickness = 2

        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_x = rect_start_point[0] + (rect_w - text_w) // 2
        text_y = rect_start_point[1] + (rect_h + text_h) // 2

        # 위험 표시 방식 선택: 원형(색상만) 또는 사각형(색상+텍스트)
        if circle_mode:
            # 우측 상단에 원형 인디케이터
            center_point = INI_CONFIG.global_config.danger_indicator_location
            radius = INI_CONFIG.global_config.danger_indicator_radius
            danger_frame = cv2.circle(danger_frame, center_point, radius, frame_color, -1, lineType=cv2.LINE_4)
        else:
            # 우측 상단에 텍스트 박스
            danger_frame = cv2.rectangle(danger_frame, rect_start_point, rect_end_point, frame_color, -1)
            danger_frame = cv2.putText(
                danger_frame, text, (text_x, text_y), font,
                font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA
            )

        # 4. 테두리 그리기 (옵션)
        if draw_border:
            height, width, _ = danger_frame.shape
            border_thickness = 10
            # danger_frame = cv2.copyMakeBorder(
            #     src = danger_frame,
            #     top = border_thickness, bottom = border_thickness, left = border_thickness, right = border_thickness,
            #     borderType = cv2.BORDER_CONSTANT, value = frame_color
            # )
            danger_frame = cv2.rectangle(danger_frame, (0, 0), (width - 1, height - 1), frame_color, border_thickness)
        return danger_frame
    
    def _draw_cctv_name_on_frame(self, frame_bgr: np.ndarray):
        """
        CCTV 화면 왼쪽에 개소명 표기
        글자 길이에 맞게 rectangle 구성
        """
        camera_name = self.config.camera_info["camera_name"]
        font_size = 24
        text_color = (255, 255, 255)  # 흰색 텍스트
        bg_color = (127, 127, 127)  # 배경색

        # FreeType으로 텍스트 크기 계산
        (text_width, text_height), baseline = self.ft.getTextSize(camera_name, font_size, -1)
        
        # 배경 사각형 좌표 (여백 포함)
        padding = 10
        rect_x1, rect_y1 = 5, 10
        rect_x2 = rect_x1 + text_width + padding * 2
        rect_y2 = rect_y1 + text_height + padding * 2
        
        # 개소 표기용 rectangle (글자 길이에 맞춰 동적 크기)
        frame_bgr = cv2.rectangle(frame_bgr, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
        
        # 텍스트 좌표 (사각형 내부에 적절히 배치)
        text_x = rect_x1 + padding
        text_y = rect_y1 + text_height + padding
        
        # 카메라명 표시 <- 한글 입력 위해 FreeType 사용
        frame_bgr = self.ft.putText(frame_bgr, camera_name, (text_x, text_y), font_size, text_color, -1, cv2.LINE_8, True)

        return frame_bgr
    
    def _draw_person_counter_on_frame(self, frame_bgr: np.ndarray):
        """
        현재 영상에 사람 카운터 로직이 존재할 경우 프레임 우측 하단에 작업자 수 표기
        """
        if self.person_count is None or self.person_count < 0:
            return frame_bgr
        
        text = f"person: {self.person_count}"
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 2
        text_color = (255, 255, 255)  # 흰색 텍스트
        bg_color = (200, 100, 100)  # 배경색

        # 텍스트 크기 계산
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
        
        # 배경 사각형 좌표 (여백 포함)
        padding = 10
        height, width, _ = frame_bgr.shape
        rect_x2, rect_y1 = width - 5, height - 40
        rect_x1 = rect_x2 - text_width - padding * 2
        rect_y2 = rect_y1 + text_height + padding * 2
        
        # 작업자 수 표기용 rectangle (글자 길이에 맞춰 동적 크기)
        frame_bgr = cv2.rectangle(frame_bgr, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
        
        # 텍스트 좌표 (사각형 내부에 적절히 배치)
        text_x = rect_x1 + padding
        text_y = rect_y1 + text_height + padding
        
        # 작업자 수 표시
        frame_bgr = cv2.putText(frame_bgr, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
        return frame_bgr
    #endregion

    #region 이벤트 스레드(Detection Loop) 유틸 함수
    @staticmethod
    def _predict(config: VideoConfig, frame_bgr: np.ndarray, models: dict[str, YOLO]) -> dict[str, "Results"]:
        """
        입력: models = { model_name: YOLO }
        출력: { model_name: results[0] }  # Ultralytics Results 객체
        """
        results_by_model: dict[str, "Results"] = {}

        for model_name, model in models.items():
            if model is None:
                continue

            # track 사용 시 persist=True면 모델 인스턴스별 트래커 상태가 유지됨
            # -> 동일 인스턴스를 여러 이벤트/스레드가 공유하지 않도록 설계할 것
            results = model.track(frame_bgr, device=config.device, conf=config.confidence_threshold, verbose=False, persist=True, tracker=paths.TRACKER_LOCATION)
            results_by_model[model_name] = results[0]

        return results_by_model

    def _create_danger_detection(self, results_by_model: dict[str, "Results"], class_filters: dict[str, set[int]]) -> list[dict]:
        """
        results_by_model: { model_name: Results }
        class_filters:    { model_name: {class_index, ...} }  # 없으면 전체 허용
        """
        
        detections: list[dict] = []

        for model_name, res in results_by_model.items():
            allow: set[int] | None = class_filters.get(model_name, None)  # None이면 전체 허용
            boxes = getattr(res, "boxes", None)
            if boxes is None:
                continue

            # to numpy
            xyxy = boxes.xyxy.detach().cpu().numpy() if boxes.xyxy is not None else None
            cls  = boxes.cls.detach().cpu().numpy().astype(int) if boxes.cls is not None else None
            conf = boxes.conf.detach().cpu().numpy() if boxes.conf is not None else None
            if xyxy is None or cls is None or conf is None:
                continue

            n = xyxy.shape[0]
            if n == 0:
                continue

            # track id 정규화
            tid_t = getattr(boxes, "id", None)
            if tid_t is None:
                track_ids = np.full(n, -1, dtype=int)
            else:
                track_ids = tid_t.detach().view(-1).cpu().numpy().astype(int)
                if track_ids.shape[0] < n:
                    track_ids = np.pad(track_ids, (0, n - track_ids.shape[0]), constant_values=-1)
                elif track_ids.shape[0] > n:
                    track_ids = track_ids[:n]

            # 항목 단위로 target_allowed 계산(태깅)
            for (x1, y1, x2, y2), cls_id, score, track_id in zip(xyxy, cls, conf, track_ids):
                x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
                cls_id = int(cls_id)
                score  = float(score)
                track_id = int(track_id)

                if track_id == -1:
                    continue  # 추적 ID가 없는 객체는 무시

                # allow가 None이면 전체 허용, 그렇지 않으면 set membership 테스트
                target_allowed = True if (allow is None or cls_id in allow) else False

                detections.append({
                    "track_id": track_id,
                    "class_id": cls_id,
                    "confidence": score,
                    "bbox": (x1, y1, x2, y2),
                    "filter": target_allowed,
                })
        return detections

    def _check_ai_detection_result_by_dynamic_event_process(self, event_index: int, detections: List[dict]) -> bool:
        """
        detections =  [
            {'track_id': 12, 'class_id': 0, 'confidence': 0.9599609375, 'bbox': (500, 338, 558, 464)},
            {'track_id': 13, 'class_id': 1, 'confidence': 0.953125, 'bbox': (507, 352, 553, 417)},
            {'track_id': 14, 'class_id': 3, 'confidence': 0.85986328125, 'bbox': (461, 184, 480, 214)}
        ]
        """
        if not detections:
            return False
        
        # 이벤트 인덱스에 해당하는 필터 정보 가져오기
        cctv_name = self.event_log.cctv_name
        results = self.event_logic.universal_dynamic_event_process(cctv_name=cctv_name, event_index=event_index,
                                                                    detection_data=detections, frame_buffer=self.frame_buffer,
                                                                    filter_dict=self.filter_dict)

        # TODO: 2025-09-24 작업자 수 집계 결과 처리용 변수 (현재 미사용)
        if type(results) is int:
            self.person_count: int = results
        else:
            return results

    def _find_algorithm_from_config(self, event_index: int) -> Optional[str]:
        """
        설정(config)을 순회하며 첫 번째로 발견되는 알고리즘의 이름을 반환합니다.
        발견하지 못하면 None을 반환합니다.
        """
        algorithm_list = []
        for event in self.config.event:
            for model in event.get("models", []):
                if model.get("type") == "algorithm":
                    algorithm_list.append(model.get("name"))
        if algorithm_list:
            return algorithm_list[event_index]
        else:
            return None

    def _set_current_algorithm(self, event_index: int):
        """
        지정된 event_index에 대한 현재 알고리즘을 설정합니다.
        이미 설정된 경우, 아무 작업도 수행하지 않습니다.
        """
        if self.current_algorithm.get(event_index) not in (None, "None"):
            return

        found_name = self._find_algorithm_from_config(event_index)
        if found_name:
            known_algorithm = set(INI_CONFIG.logic_dict.keys())
            algorithm_to_set = (
                found_name if found_name in known_algorithm else "기타"
            )
            self.current_algorithm[event_index] = algorithm_to_set

        self.logger.info(f"{self.current_algorithm.get(event_index)}")

    def _handle_danger_detection(self, event_index:int, danger_type: DangerType, current_time: float, danger_maintain_time: float = INI_CONFIG.global_config.danger_maintain_time):
        """위험 상황 처리"""
        event_name = self.config.event[event_index]['name']
        
        if not self.is_danger:
            # 최초 위험 감지
            self.is_danger = True
            if danger_type == DangerType.JIGUK_DANGER:
                pass
            else:
                self._create_event_log(event_index, current_time)
            self._send_danger_notification(event_index, event_name, danger_type)
        # 기존 타이머 취소 후 새로 시작 (타이머 갱신)
        if self.danger_timer:
            self.danger_timer.cancel()
        
        self.danger_timer = threading.Timer(danger_maintain_time, self._reset_danger)
        self.danger_timer.start()

    def _reset_danger(self):
        """위험 상태 해제"""
        self.is_danger = False
        self.danger_timer = None
        self.roi = []
        self._send_danger_notification("-", None, is_reset=True)
    
    def _send_danger_notification(self, event_index, event_name: str, danger_type: DangerType = None, is_reset: bool = False, is_jiguk_performed: bool = False):
        """위험 상태 또는 리셋 알림을 event_grid_queue로 전송"""
        try:
            event_risk_level = -1 if is_reset else self.config.event[0]["risk_level"]

            # 위험 상태 유지 시간 결정
            danger_maintain_time = INI_CONFIG.global_config.danger_maintain_time
            current_algorithm = self.current_algorithm.get(event_index)

            for algorithm_name in self.algorithm_configs.keys():
                if danger_type == DangerType.JIGUK_DANGER:
                    danger_maintain_time = self.algorithm_configs["지적확인"]["danger_maintain_time"]
                    break
                elif current_algorithm == algorithm_name:
                    danger_maintain_time = self.algorithm_configs[algorithm_name]["danger_maintain_time"]
                    break

            self.event_log.danger_maintain_time = danger_maintain_time

            display_event = DisplayGridData(
                cctv_location=self.event_log.cctv_location,
                cctv_name=self.event_log.cctv_name,
                event_name=event_name,
                event_risk_level=event_risk_level,
                jiguk_performed=is_jiguk_performed,
                danger_maintain_time= self.event_log.danger_maintain_time
            )
            frame_data = EventGridData(
                cctv_info=self.config,
                display_event=display_event,
            )
            self._safe_put_queue(self.event_grid_queue, frame_data)

        except Exception as e:
            self.logger.error(f"위험 상태 {('리셋 ' if is_reset else '')}알림 전송 오류: {e}")

    def _safe_put_queue(self, mp_queue: mp.Queue, item):
        """큐에 안전하게 아이템을 넣습니다. 큐가 가득 찼을 경우 기존 아이템을 비우고 다시 시도합니다."""
        try:
            mp_queue.put_nowait(item)
        except queue.Full:
            # self.logger.warning("큐가 가득 찼습니다. 큐를 비우고 다시 시도합니다.")
            while not mp_queue.empty():
                try:
                    mp_queue.get_nowait()
                except queue.Empty:
                    break
            try:
                mp_queue.put_nowait(item)
            except:
                pass
                # self.logger.error("큐에 아이템을 넣는 데 실패했습니다.")
    #endregion

    #region 이벤트 로그 생성
    def _create_event_log(self, event_index:int, current_time: float):
        """
        2025-06-17  
        event_log에서 cctv_location과 cctv_name이 tuple인 값과 str인 값이 혼재되어 들어오고 있음

        2025-07-08  
        TODO: _save_video()가 이벤트 발생 직후 영상을 저장하고 있음 -> 이벤트 발생 직전의 프레임을 저장하려면 로직을 변경해야함
        """
        self.event_log.timestamp = current_time
        self.event_log.cctv_location = self.event_log.cctv_location
        self.event_log.cctv_name = self.event_log.cctv_name
        self.event_log.event_name = self.config.event[0]["name"] # <-- 이부분 수정해야함

        # frame_bgr = self.prev_result.plot()
        frame_bgr = self.frame_bgr.copy()
        plot_frame = self._custom_plot(frame_bgr)
        first_event_algorithm = self.current_algorithm.get(0, "")
        if first_event_algorithm in self.algorithm_configs.keys():
            plot_frame = self._extend_bbox_visualization(plot_frame)
        frame_bgr_cropped = self._scale_frame_to_letterbox(plot_frame)
        frame_danger = self._process_danger_frame(frame_bgr_cropped)

        self._save_snapshot(frame_danger)
        # self._save_video()
        self._send_event_log(event_index)
        # self.logger.info(f"이벤트 로그 생성: {event_log}")

    def _get_file_path_info(self, subfolder: str, extension: str) -> tuple[str, str, Path]:
        """파일 저장을 위한 공통 경로 정보 생성"""
        current_date = time.strftime("%Y-%m-%d", time.localtime(self.event_log.timestamp))
        current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(self.event_log.timestamp))

        # TODO: 절대경로 RIST 컴퓨터에 업로드할 때에는 /home/rist/...로 변경해야함
        target_path = Path(f"{PROJECT_ROOT}/{subfolder}/{current_date}")
        target_path.mkdir(parents=True, exist_ok=True)
        
        file_path = target_path / f"{current_time}_{self.event_log.cctv_name}.{extension}"
        return current_date, current_time, file_path

    def _save_snapshot(self, frame_bgr: np.ndarray):
        """
        2025-06-17
        이미지 저장 경로 변경 및 이벤트 이름 임시 제외

        기존:
        /home/rist/rist-ai-cctv-2025-2nd/web/static/images/issue_log/2025-05-28/20250528_162330_CCTV 100_HamanFall.jpeg

        변경:
        /home/rist/rist-ai-cctv-2025-2nd/img/2025-06-17/20250617_141850_CCTV 2.jpg

        EventLogData(
            timestamp=1750137644.6040177,
            cctv_location='1공장',
            cctv_name='CCTV 2',
            event_name='사람과 차',
            image_path='/home/rist/rist-ai-cctv-2025-2nd/img/2025-06-17/20250617_142044_CCTV 2.jpg'
        )
        """
        _, _, image_path = self._get_file_path_info("img", "jpg")
        self.event_log.image_path = str(image_path)
        cv2.imwrite(str(image_path), frame_bgr)
        del frame_bgr

    def _save_video(self):
        """위험상황 발생 직후 약 n초(RECORD_DURATION)간 영상을 저장하는 로직"""
        try:
            _, _, video_path = self._get_file_path_info("video", "mp4")
            self.video_writer = VideoWriter(str(video_path), self.frame_bgr.shape[:2][::-1])
            self.video_writer.start_recording()
        except Exception as e:
            self.logger.error(f"비디오 저장 초기화 오류: {e}")

    def _send_event_log(self, event_index: int):
        """이벤트 로그를 메인 프로세스로 전송"""
        try:
            # 이벤트 로그만 전송하는 특별한 FrameData 생성
            if not self.config.event or event_index >= len(self.config.event):
                # self.logger.warning(f"유효하지 않은 이벤트 인덱스: {event_index}")
                return
            
            # 위험 상태 유지 시간 결정
            danger_maintain_time = INI_CONFIG.global_config.danger_maintain_time
            current_algorithm = self.current_algorithm.get(event_index)

            for algorithm_name in self.algorithm_configs.keys():
                if current_algorithm == algorithm_name:
                    danger_maintain_time = self.algorithm_configs[algorithm_name]["danger_maintain_time"]
                    break

            self.event_log.danger_maintain_time = danger_maintain_time

            # 위험 레벨 설정
            try:
                event_data: dict = self.config.event[event_index]
                risk_level_value = event_data.get("risk_level", "danger_mid")
                risk_level = RiskLevel_1(risk_level_value)
            except Exception as e:
                risk_level = RiskLevel_1.danger_mid

            event_frame_data = FrameData(
                cctv_info=self.config,
                event_log=self.event_log,
                frame=None,  # 이벤트 로그 전용이므로 프레임은 None
                detections=[],
                is_event_notification=True,  # 이벤트 로그 전용 플래그 (필요시 추가)
                severity=risk_level.name,
            )
            
            self.output_queue.put_nowait(event_frame_data)
            # self.logger.info(f"이벤트 로그 전송 완료: {event_log.event_name}")
            
        except queue.Full:
            # self.logger.warning("출력 큐가 가득 참 - 이벤트 로그 전송 실패")
            # pass
            while not self.output_queue.empty():
                try:
                    self.output_queue.get_nowait()
                except queue.Empty:
                    break
        except Exception as e:
            self.logger.error(f"이벤트 로그 전송 오류: {e}")
    #endregion

    #region 유틸 함수
    def _send_stream_status(self, is_healthy: bool):
        """스트림 상태를 output_queue로 전송"""
        try:
            status_data = {
                "type": "stream_status",
                "video_number": self.config.video_number,
                "is_healthy": is_healthy,
                "timestamp": time.time()
            }
            self.output_queue.put_nowait(status_data)
        except queue.Full:
            pass
        except Exception as e:
            self.logger.error(f"스트림 상태 전송 오류: {e}")

    def _convert_gpu_frame_to_cpu_frame(self, gpu_frame: cv2.cuda.GpuMat) -> np.ndarray:
        """
        2025-07-04
        기존 cv2.resize에서 Letterboxing 처리로 변경
        """
        try:
            width, height = gpu_frame.size()
            target_size = 640
            
            # aspect ratio 유지하면서 리사이징할 비율 계산
            ratio = min(target_size / width, target_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # GPU에서 리사이징
            gpu_frame_resized = cv2.cuda.resize(gpu_frame, (new_width, new_height))
            
            # 패딩 계산
            top = (target_size - new_height) // 2
            bottom = target_size - new_height - top
            left = (target_size - new_width) // 2
            right = target_size - new_width - left

            # letterbox_info 저장
            # letterbox_info는 원본 크기, 타겟 크기, 비율
            # 패딩 정보는 top, bottom, left, right
            self.letterbox_info = {
                "origWidth": width,
                "origHeight": height,
                "targetSize": target_size,
                "ratio": ratio,
                "top": top,
                "left": left
            }

            # GPU에서 패딩 추가 (letterboxing)
            gpu_frame_padded = cv2.cuda.copyMakeBorder(
                gpu_frame_resized, 
                top, bottom, left, right, 
                cv2.BORDER_CONSTANT, 
                value=(114, 114, 114, 0)  # BGRA 형식이므로 4채널
            )
            
            # CPU로 다운로드 및 색상 변환
            cpu_frame_bgr = gpu_frame_padded.download()
            final_frame_bgr = cv2.cvtColor(cpu_frame_bgr, cv2.COLOR_BGRA2BGR)
            del gpu_frame_resized
            del cpu_frame_bgr
            return final_frame_bgr
        except:
            gc.collect()
            raise

    def _scale_bbox_to_original(self, bbox, letterbox_info):
        # bbox: [x1, y1, x2, y2] (640x640 기준)
        x1, y1, x2, y2 = bbox
        ratio = letterbox_info["ratio"]
        left = letterbox_info["left"]
        top = letterbox_info["top"]
        orig_width = letterbox_info["origWidth"]
        orig_height = letterbox_info["origHeight"]

        # 레터박스 영역 제외 후 원본 비율로 변환
        x1 = max((x1 - left) / ratio, 0)
        y1 = max((y1 - top) / ratio, 0)
        x2 = min((x2 - left) / ratio, orig_width)
        y2 = min((y2 - top) / ratio, orig_height)
        return [int(x1), int(y1), int(x2), int(y2)]

    def _scale_frame_to_letterbox(self, frame_bgr: np.ndarray):
        # 레터박스 영역만 crop
        left = self.letterbox_info["left"]
        top = self.letterbox_info["top"]
        target_size = self.letterbox_info["targetSize"]
        new_width = target_size - 2 * left
        new_height = target_size - 2 * top
        frame_bgr_cropped = frame_bgr[top:top + new_height, left:left + new_width]

        # bbox 변환 -> 2025-8-13 미사용 변수?
        # detections_orig = []
        # for det in self.latest_detections:
        #     bbox_orig = self._scale_bbox_to_original(det["bbox"], self.letterbox_info)
        #     detections_orig.append({
        #         "track_id": det["track_id"],
        #         "class_id": det["class_id"],
        #         "confidence": det["confidence"],
        #         "bbox": bbox_orig
        #     })
        return frame_bgr_cropped

    def _store_frame_in_deque(self, gpu_frame: cv2.cuda.GpuMat):
        """
        GPU 프레임을 deque에 저장
        deque는 최대 MAX_RECORD_BUFFER_SIZE(150) 프레임까지만 저장
        """
        frame_bgra = gpu_frame.download()
        frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
        with self.frame_buffer_lock:
            if self.prev_result:
                self.frame_buffer.append((frame_bgr, self.prev_result))
            else:
                self.frame_buffer.append((frame_bgr, None))

    @staticmethod
    def _calculate_iou(box1: torch.Tensor, box2: torch.Tensor) -> float:
        """두 바운딩 박스 간의 IoU(Intersection over Union)를 계산합니다."""
        # box 좌표는 xyxy 형식이라고 가정합니다.
        x1_inter = max(box1[0], box2[0])
        y1_inter = max(box1[1], box2[1])
        x2_inter = min(box1[2], box2[2])
        y2_inter = min(box1[3], box2[3])

        # 교차 영역의 넓이를 계산합니다.
        intersection_area = max(0, x2_inter - x1_inter) * max(0, y2_inter - y1_inter)
        if intersection_area == 0:
            return 0.0

        # 각 박스의 넓이를 계산합니다.
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

        # 합집합(Union)의 넓이를 계산합니다.
        union_area = box1_area + box2_area - intersection_area

        # IoU를 계산하고 반환합니다.
        iou = intersection_area / union_area
        return iou.item() # tensor에서 float 값으로 변환

    @staticmethod
    def _calculate_intersection_area( box1: torch.Tensor, box2: torch.Tensor) -> float:
        """두 바운딩 박스 간의 교차 영역 넓이를 계산합니다."""
        x1_inter = max(box1[0], box2[0])
        y1_inter = max(box1[1], box2[1])
        x2_inter = min(box1[2], box2[2])
        y2_inter = min(box1[3], box2[3])
        
        intersection_area = max(0, x2_inter - x1_inter) * max(0, y2_inter - y1_inter)
        return intersection_area.item()

    def _calculate_containment_ratio(self, box_to_check: torch.Tensor, container_box: torch.Tensor) -> float:
        """'box_to_check'가 'container_box'에 얼마나 포함되는지 비율을 계산합니다."""
        intersection_area = self._calculate_intersection_area(box_to_check, container_box)
        box_to_check_area = (box_to_check[2] - box_to_check[0]) * (box_to_check[3] - box_to_check[1])

        if box_to_check_area == 0:
            return 0.0
        
        return intersection_area / box_to_check_area.item()

    def _find_intersecting_frame_index(self, buffer: deque, target_id: int, intersecting_cls: int = 1, intersect_threshold: float = 0.01) -> int | None:
        """
        버퍼를 순회하며 지정된 ID의 객체와 지정된 클래스의 객체가
        IoU 임계값 이상으로 겹치는 첫 번째 프레임의 인덱스를 찾습니다.

        Args:
            buffer (deque): (frame, results) 쌍을 담고 있는 deque.
            target_id (int): 추적 대상 객체의 ID.
            intersecting_cls (int): 교차를 확인할 객체의 클래스 인덱스.
            iou_threshold (float): IoU 임계값.

        Returns:
            int | None: 조건을 만족하는 프레임의 인덱스. 찾지 못하면 None을 반환.
        """
        intersect_list = []

        # buffer의 각 프레임과 결과에 대해 반복
        # range(len(buffer) - 1, -1, -1)는 마지막 인덱스부터 0까지 역으로 순회합니다.
        for i in range(len(buffer) - 1, -1, -1):
            # 역순 인덱스로 프레임과 결과에 접근
            frame, results = buffer[i]
            results: Results = results
            try:
                boxes = results.boxes
            except:
                # results 객체가 비정상일 경우 다음 프레임으로 넘어감
                continue

            if boxes.id is None:
                continue

            all_ids = boxes.id.int()
            all_cls = boxes.cls.int()
            all_xyxy = boxes.xyxy

            target_indices = torch.where(all_ids == target_id)[0]
            intersecting_indices = torch.where(all_cls == intersecting_cls)[0]

            if len(target_indices) > 0 and len(intersecting_indices) > 0:
                target_bbox = all_xyxy[target_indices[0]]

                for intersect_idx in intersecting_indices:
                    intersecting_bbox = all_xyxy[intersect_idx]
                    intersect_ratio = self._calculate_containment_ratio(target_bbox, intersecting_bbox)
                    if intersect_ratio >= intersect_threshold:
                        intersect_list.append((i, intersect_ratio))

        if intersect_list and len(intersect_list) > 0:
            max_tuple = max(intersect_list, key=lambda x: x[1])
            max_index, max_intersect = max_tuple
            if max_intersect > intersect_threshold:
                return max_index
            else:
                return intersect_list[0][0]
        
        # 전체 버퍼를 역순으로 확인했지만 조건을 만족하는 프레임을 찾지 못한 경우
        default_index = -10
        return default_index

    def _schedule_next_reset(self):
        """다음 자정에 TRACKER ID 리셋 타이머를 설정"""

        now = datetime.datetime.now()

        # 설정된 시각 계산
        target_time = now.replace(
            hour=INI_CONFIG.global_config.tracker_reset_hour,
            minute=INI_CONFIG.global_config.tracker_reset_minute,
            second=0,
            microsecond=0
        )

        # 현재 시각이 목표 시각을 지났다면 다음 날로 설정
        if now >= target_time:
            target_time += datetime.timedelta(days=1)

        seconds_until_reset = (target_time - now).total_seconds()

        # 기존 타이머 취소
        if self.tracking_id_reset_timer is not None:
            self.tracking_id_reset_timer.cancel()

        # 새 타이머 설정
        self.tracking_id_reset_timer = threading.Timer(
            seconds_until_reset, 
            self._reset_track_id_count
        )
        self.tracking_id_reset_timer.daemon = True
        self.tracking_id_reset_timer.start()
        # self.logger.info(f"Tracker ID 리셋 타이머 설정: {seconds_until_reset:.0f}초 후 ({target_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    def _reset_track_id_count(self):
        """자정에 TRACKER ID 리셋"""
        try:
            # self.logger.info("자정 Tracker ID 리셋 시작")
            for event_index, models in self.models.items():
                for model_name, model in models.items():
                    if hasattr(model, "predictor") and hasattr(model.predictor, "trackers"):
                        if len(model.predictor.trackers) > 0:
                            model.predictor.trackers[0].reset()

            self._schedule_next_reset()
            
        except Exception as e:
            self.logger.error(f"Tracker ID 리셋 오류: {e}")
            self._schedule_next_reset()

    def _clear_bulti_roi(self):
        """불티비산 ROI 클리어 (타이머 콜백)"""
        self.roi = []
        self.bulti_roi_timer = None

    def cleanup(self):
        """리소스 정리"""
        self.is_running = False

        if self.detector_thread_list:
            for thread in self.detector_thread_list:
                if thread.is_alive():
                    thread.join(timeout=2.0)

        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=2.0)

        if hasattr(self, 'video_writer') and self.video_writer:
            try:
                self.video_writer.stop_recording()
                time.sleep(0.1)
            except Exception as e:
                pass
            finally:
                self.video_writer = None

        if self.gpu_reader:
            del self.gpu_reader
            self.gpu_reader = None
            
        if self.model:
            del self.model
            self.model = None
        
        if self.danger_timer:
            self.danger_timer.cancel()

        if self.bulti_roi_timer:
            self.bulti_roi_timer.cancel()
            self.bulti_roi_timer = None

        if self.tracking_id_reset_timer is not None:
            self.tracking_id_reset_timer.cancel()
        
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break
        
        self.latest_detections = []
        self.prev_result = None
        self.frame_bgr = None
        
        torch.cuda.empty_cache()
        # self.logger.info("리소스 정리 완료")
    #endregion

def video_process_main(config: VideoConfig, command_queue: mp.Queue, output_queue: mp.Queue, event_grid_queue: mp.Queue):
    process = VideoProcess(config, command_queue, output_queue, event_grid_queue)
    process.run()