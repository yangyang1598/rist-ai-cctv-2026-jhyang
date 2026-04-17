# video_config.py
import sys
import ast
import logging
from enum import Enum
from collections import deque
from dataclasses import dataclass, field, asdict
from typing import Optional, Tuple, Any, Dict, NamedTuple
from PySide6.QtWidgets import QGridLayout
from ultralytics.engine.results import Results
from setting import paths
from setting.use_qsetting import Setting
from rich.console import Console
console = Console()


def setup_logger(process_name: str) -> logging.Logger:
    """디버깅용 로거 함수 설정"""
    logger = logging.getLogger(process_name)
    if logger.handlers:
        return logger
    
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        f'[%(levelname)s] %(name)s - %(filename)s:L%(lineno)d - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


#region dataclass
@dataclass
class VideoConfig:
    """비디오 처리 설정을 담는 데이터 클래스"""
    is_visualize: bool = False # 시각화 여부 *
    video_number: int = 0 # 비디오 소스 번호
    device: int = 0  # GPU 디바이스 번호
    triton_url: str = "grpc://[::1]:8001/yolov8x_1" # Triton 서버 URL
    model_input_size: Tuple[int, int] = (640, 640) # Triton 모델 입력 크기
    confidence_threshold: float = 0.5 # 신뢰도 임계값
    queue_size: int = 3 # 프레임 큐 크기
    frame_delay_ms: int = 33 # 프레임 지연 시간 (ms)
    wait_timeout_ms: int = 3000 # 대기 타임아웃 (ms)
    event: list = field(default_factory=list)    # 이벤트 정보
    camera_info: dict = field(default_factory=dict) # CCTV 정보
    cctv_fps: float = 30.0 # CCTV FPS

    def to_dict(self) -> Dict:
        """VideoConfig 객체를 JSON 직렬화 가능한 딕셔너리로 변환"""
        return asdict(self)
    
@dataclass
class GlobalConfig:
    """전역 설정"""
    max_retry                      :int   = 5          # 영상 수신 실패 시 최대 재시도 횟수
    min_skip_frame                 :int   = 1          # 최소 스킵 프레임 수
    danger_maintain_time           :int   = 5          # 위험 상태 유지 시간 (초)
    jiguk_danger_maintain_time     :float = 2.0        # 지적확인 위험 상태 유지 시간 (초)
    bulti_danger_maintain_time     :float = 5.0        # 불티비산(훈소) 위험 상태 유지 시간 (초)
    collision_danger_maintain_time :float = 3.0        # 접근 감지 위험 상태 유지 시간 (초)
    record_duration                :int   = 5          # 이벤트로그 작성 시 영상 저장 시간 (초)
    sequence_buffer_size           :int   = 30         # 연속 검출 시 프레임 데이터 저장용 deque 크기 (프레임 수)
    jiguk_buffer_size              :int   = 30         # 연속 검출 시 지적확인 행동 검출 여부 저장용 deque 크기 (프레임 수)
    tracker_max_id_count           :int   = 1000       # YOLO Tracker에 저장할 최대 ID 카운트
    max_record_buffer_size         :int   = 90         # 녹화 시 최대 프레임 버퍼 크기 (프레임 수)
    roi_extend_pixel               :int   = 50         # ROI 확장 픽셀 수
    system_check_time              :int   = 60         # 시스템 상태 점검 주기 (초)
    tracker_reset_hour             :int   = 0          # TRACKER ID 리셋 시각 (시)
    tracker_reset_minute           :int   = 0          # TRACKER ID 리셋 시각 (분)
    line_width                     :int   = 2          # BBOX 시각화 선 두께
    danger_indicator_circle_mode   :bool  = True       # 위험 인디케이터 모드 (원형: True, 사각형: False)
    danger_indicator_location      :tuple = (620, 20)  # 위험 인디케이터 위치 (픽셀, 픽셀)
    danger_indicator_radius        :int   = 15         # 위험 인디케이터 반지름 (픽셀)

@dataclass
class SessionConfig:
    """지적확인 세션 관련 설정"""
    leave_grace_sec: float = 0.6
    cooldown_sec: float = 2.0
    min_dwell_sec: float = 10.0
    min_move_px: int = 5

@dataclass
class BultiConfig:
    """불티비산(훈소) 감지 설정"""
    roi_extend_pixel: int = 100
    roi_maintain_time: int = 10

@dataclass
class CollisionConfig:
    """접근감지 설정"""
    roi_extend_pixel: int = 50
    min_collision_frames: int = 5
    max_window_frames: int = 10

@dataclass
class SafebeltConfig:
    """안전대&안전벨트 설정"""
    roi_extend_pixel: int = 50
    logic_1_detect_time: int = 2
    logic_2_detect_time: int = 2

@dataclass
class FlashSuitConfig:
    """보호구 감지 설정"""
    roi_extend_pixel: int = 100
    detect_time: int = 2

    
@dataclass
class EventLogData:
    """이벤트 로그 데이터 클래스"""
    timestamp: float = 0.0
    cctv_location: str = ""
    cctv_name: str = ""
    event_name: str = ""
    event_risk_level: int = -1
    image_path: str = ""
    danger_maintain_time: float = 30.0
    severity: str = ""  # 위험도
    
@dataclass
class FrameData:
    """
    프로세스 간 전송되는 프레임 데이터
    이벤트 로그 전송용
    """
    cctv_info: VideoConfig = field(default_factory=VideoConfig)  # CCTV 정보
    event_log: EventLogData = field(default_factory=EventLogData)  # 이벤트 로그 데이터
    frame: Optional[Any] = None  # 프레임 데이터 (예: numpy 배열)
    detections: list = field(default_factory=list) # 탐지 결과
    is_event_notification: bool = False # 이벤트 알림 
    severity: str = "" # 위험도

@dataclass
class DisplayGridData:
    """이벤트 상태 표기 데이터 클래스"""
    cctv_location: str = ""
    cctv_name: str = ""
    event_name: str = ""
    event_risk_level: int = -1
    jiguk_performed: bool = False
    danger_maintain_time: float = 30.0
    
@dataclass
class EventGridData:
    """이벤트 상태 그리드용 데이터"""
    cctv_info: VideoConfig = field(default_factory=VideoConfig)  # CCTV 정보
    display_event: DisplayGridData = field(default_factory=DisplayGridData)  # 이벤트 로그 데이터

@dataclass
class PtzData:
    """PTZ 제어 데이터 클래스"""
    camera_ip: str = "192.168.88.174", 
    camera_port: int = 8554,
    rtsp_id: str = "",
    rtsp_pw: str = ""

@dataclass
class LayoutData:
    """레이아웃 저장용 데이터 클래스"""
    row: int = 1
    col: int = 1
    grid: QGridLayout = field(default_factory=QGridLayout)
    cctv_info: VideoConfig = field(default_factory=VideoConfig)

@dataclass
class JigukSessionData:
    """지적확인 세션 데이터 클래스"""
    event_index: int = -1
    session_id: str = ""
    start_time: float = 0.0
    end_time: float = 0.0
    jiguk_check_deque: deque = field(default_factory=deque)
    jiguk_performed: bool = False
    consecutive_no_intersection: int = 0
    jiguk_direction: str = ""
    direction_result_str: str = ""
    initial_center: Optional[Tuple[float, float]] = None
    final_center: Optional[Tuple[float, float]] = None
    last_time_in_space: float= 0.0
    last_seen_time: float = 0.0
    time_when_left_space: float = 0.0
    current_state: str = ""
    yolo_result_on_exit: Optional[Results] = None
    yolo_result_on_jiguk: Optional[Results] = None

@dataclass
class PerformanceData:
    """프로세스 성능 데이터"""
    cctv_name: str = ""
    current_frame: int = 0
    original_fps: float = 0.0
    client_side_frame_rate: float = 0.0
    client_side_rps: float = 0.0
    event_dict: dict = ""
#endregion

#region Enum
class VideoState(Enum):
    IDLE = "Idle" # 대기 상태
    RUNNING = "Running" # 실행 중 상태
    STOPPED = "Stopped" # 중지 상태
    ERROR = "Error" # 오류 상태

class MessageType(Enum):
    """프로세스 간 메시지 타입"""
    START_VIDEO = "start_video" # 비디오 시작
    STOP_VIDEO = "stop_video" # 비디오 중지
    RECONNECT = "reconnect" # 스트림 재연결
    UPDATE_VISUALIZATION = "update_visualization" # 시각화 업데이트
    FRAME_DATA = "frame_data" # 프레임 데이터 전송
    SHUTDOWN = "shutdown" # 프로세스 종료
    RECORD = "start_recording" # 녹화 중 상태

class DangerType(Enum):
    """위험 상황 타입"""
    JIGUK_DANGER: int = 1 # 지적확인 위험
    OTHER_DANGER: int = 2 # 기타 위험
    
class SessionState(Enum):
    """세션 상태머신"""
    IN = "IN"
    OUT_PENDING = "OUT_PENDING"
    OUT = "OUT"

class DirectionType(Enum):
    """지적확인 방향성판단용 타입"""
    LEFT = (1, "LEFT", "오른쪽에서 왼쪽으로 이동")
    RIGHT = (2, "RIGHT", "왼쪽에서 오른쪽으로 이동")
    UP = (3, "UP", "아래에서 위로 이동")
    DOWN = (4, "DOWN", "위에서 아래로 이동")
    NONE = (None, "NONE", "데이터 없음")

    def __init__(self, db_value, config_str, result_str):
        self.db_value = db_value
        self.config_str = config_str
        self.result_str = result_str

    @classmethod
    def from_db(cls, value: int):
        for member in cls:
            if member.db_value == value:
                return member
        return cls.NONE
    
class ColorType(Enum):
    """색상 타입"""
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    YELLOW = (0, 255, 255)
    CYAN = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
class RiskLevel(Enum):
    """이벤트 위험도 레벨"""
    WARNING: int = 0
    CAUTION: int = 1
    BAD: int = 2
    GOOD: int = 3

class RiskLevel_1(Enum):
    """이벤트 위험도 레벨 텍스트"""
    danger_lowlow: int = 0  # caution
    danger_low: int = 1     # caution
    danger_mid: int = 2     # warning
    danger_high: int = 3    # warning
    danger_highhigh: int = 4  # warning
    good_mid: int = 5       # good
    good_high: int = 6      # good
    good_highhigh: int = 7  # good
    
class FrameStatus(NamedTuple):
    """영상 위험상태 표시용 네임드 튜플"""
    text: str
    color: ColorType  # BGR

#endregion
 
class ConfigManager:
    """설정 관리 싱글톤 클래스"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._setting = Setting(paths.GLOBAL_SETTING_PATH)
        self._config_dict = self._setting.to_dict()
        
        # 설정 로드
        self.global_config = self._load_global_config()
        self.logic_dict = self._config_dict.get("logic_list", {})
        
        # 알고리즘별 설정 로드
        self.session_config = self._load_session_config()
        self.bulti_config = self._load_bulti_config()
        self.collision_config = self._load_collision_config()
        self.safebelt_config = self._load_safebelt_config()
        self.flash_suit_config = self._load_flash_suit_config()
        
        self._initialized = True
    
    def _load_global_config(self) -> GlobalConfig:
        """전역 설정 로드"""
        global_data = self._config_dict.get("global", {})

        # INI/JSON은 튜플을 문자열로 저장하므로 ast.literal_eval로 안전하게 파싱
        circle_mode_str: str = global_data.get("danger_indicator_circle_mode", "True")
        circle_mode: bool = circle_mode_str.lower() == "true"
        danger_indicator_location_str: str = global_data.get("danger_indicator_location", "(620, 20)")
        danger_indicator_location: tuple[int, int] = ast.literal_eval(danger_indicator_location_str)

        return GlobalConfig(
            max_retry=int(global_data.get("max_retry", 3)),
            min_skip_frame=int(global_data.get("min_skip_frame", 3)),
            danger_maintain_time=float(global_data.get("danger_maintain_time", 30.0)),
            jiguk_danger_maintain_time=float(global_data.get("jiguk_danger_maintain_time", 2.0)),
            bulti_danger_maintain_time=float(global_data.get("bulti_danger_maintain_time", 5.0)),
            collision_danger_maintain_time=float(global_data.get("collision_danger_maintain_time", 5.0)),
            record_duration=float(global_data.get("record_duration", 5.0)),
            sequence_buffer_size=int(global_data.get("sequence_buffer_size", 30)),
            jiguk_buffer_size=int(global_data.get("jiguk_buffer_size", 30)),
            tracker_max_id_count=int(global_data.get("tracker_max_id_count", 1000)),
            max_record_buffer_size=int(global_data.get("max_record_buffer_size", 150)),
            roi_extend_pixel=int(global_data.get("roi_extend_pixel", 50)),
            system_check_time=int(global_data.get("system_check_time", 60)),
            tracker_reset_hour=int(global_data.get("tracker_reset_hour", 0)),
            tracker_reset_minute=int(global_data.get("tracker_reset_minute", 0)),
            line_width=int(global_data.get("line_width", 2)),
            danger_indicator_circle_mode=circle_mode,
            danger_indicator_location=danger_indicator_location,
            danger_indicator_radius=int(global_data.get("danger_indicator_radius", 15)),
        )
    
    def _load_session_config(self) -> SessionConfig:
        """세션 설정 로드"""
        session_data = self._config_dict.get("session", {})
        return SessionConfig(
            leave_grace_sec=float(session_data.get("leave_grace_sec", 0.6)),
            cooldown_sec=float(session_data.get("cooldown_sec", 2.0)),
            min_dwell_sec=float(session_data.get("min_dwell_sec", 10.0)),
            min_move_px=int(session_data.get("min_move_px", 5)),
        )
    
    def _load_bulti_config(self) -> BultiConfig:
        """불티비산 설정 로드"""
        bulti_data = self._config_dict.get("bulti", {})
        return BultiConfig(
            roi_extend_pixel=int(bulti_data.get("roi_extend_pixel", 100)),
            roi_maintain_time=int(bulti_data.get("roi_maintain_time", 10))
        )
    
    def _load_collision_config(self) -> CollisionConfig:
        """접근감지 설정 로드"""
        collision_data = self._config_dict.get("collision", {})
        return CollisionConfig(
            roi_extend_pixel=int(collision_data.get("roi_extend_pixel", 50)),
            min_collision_frames=int(collision_data.get("min_collision_frames", 5)),
            max_window_frames=int(collision_data.get("max_window_frames", 10)),
        )
    
    def _load_safebelt_config(self) -> SafebeltConfig:
        """안전대&안전벨트 설정 로드"""
        safebelt_data = self._config_dict.get("safebelt", {})
        return SafebeltConfig(
            roi_extend_pixel=int(safebelt_data.get("roi_extend_pixel", 50)),
            logic_1_detect_time=int(safebelt_data.get("logic_1_detect_time", 2)),
            logic_2_detect_time=int(safebelt_data.get("logic_2_detect_time", 2)),
        )
    
    def _load_flash_suit_config(self) -> FlashSuitConfig:
        """보호구 감지 설정 로드"""
        flash_suit_data = self._config_dict.get("flash_suit", {})
        return FlashSuitConfig(
            roi_extend_pixel=int(flash_suit_data.get("roi_extend_pixel", 100)),
            detect_time=int(flash_suit_data.get("detect_time", 2)),
        )
    
    def reload(self):
        """설정 파일 재로드"""
        self._setting.reload()
        self._config_dict = self._setting.to_dict()
        self.global_config = self._load_global_config()
        self.logic_dict = self._config_dict.get("logic_list", {})
        self.session_config = self._load_session_config()
        self.bulti_config = self._load_bulti_config()
        self.collision_config = self._load_collision_config()
        self.safebelt_config = self._load_safebelt_config()
        self.flash_suit_config = self._load_flash_suit_config()
        