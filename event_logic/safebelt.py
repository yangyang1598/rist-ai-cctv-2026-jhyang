# logic_test.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inspect
import io
import time
import multiprocessing as mp
import cv2
import numpy as np
import pandas as pd
from typing import List
from collections import defaultdict, deque
from ultralytics import YOLO
from ultralytics.engine.results import Results
from setting import paths
from setting.use_qsetting import Setting
from event_logic.event_logic_func import EventLogic
from event_logic.setup_event_logic import SetupEventLogic
from widget.video_process_pipeline.video_config import EventLogData, JigukSessionData, MessageType, DirectionType, SessionState

from rich.console import Console
from rich.traceback import install
console = Console()
install()

SETTING_DICT: dict =  Setting(paths.GLOBAL_SETTING_PATH).to_dict()

GLOBAL_SETTING: dict = SETTING_DICT.get("global", {})
JIGUK_BUFFER_SIZE: int = int(GLOBAL_SETTING.get("jiguk_buffer_size", 30))      # 3초 (30fps 기준)
ROI_EXTEND_PIXEL: int = int(GLOBAL_SETTING.get("roi_extend_pixel", 50))        # ROI 확장 픽셀 수

SESSION_SETTING: dict = SETTING_DICT.get("session", {})
LEAVE_GRACE_SEC: float = float(SESSION_SETTING.get("leave_grace_sec", 0.6))    # 이탈 대기 시간(초)
COOLDOWN_SEC: float = float(SESSION_SETTING.get("cooldown_sec", 2.0))          # 세션 종료 후 동일 ID 재진입 쿨다운(초)
MIN_DWELL_SEC: float = float(SESSION_SETTING.get("min_dwell_sec", 10.0))       # 지적확인 개소 내 n초 이상 체류 시 무시
MIN_MOVE_PX: int = int(SESSION_SETTING.get("min_move_px", 5))                  # 방향성 판단 최소 이동 픽셀

BULTI_SETTING: dict = SETTING_DICT.get("bulti", {})
BULTI_ROI_EXTEND = int(BULTI_SETTING.get("roi_extend_pixel", 100))

COLLISION_SETTING: dict = SETTING_DICT.get("collision", {})
COLLISION_ROI_EXTEND = int(COLLISION_SETTING.get("roi_extend_pixel", 50))
MIN_COLLISION_FRAMES = int(COLLISION_SETTING.get("min_collision_frames", 5))   # 최소 충돌 프레임 수
MAX_WINDOW_FRAMES = int(COLLISION_SETTING.get("max_window_frames", 10))        # 최대 윈도우 프레임 수

class TestEventLogic:
    def __init__(self):
        self.event_index_list: list[int] = []
        self.event_logic = SetupEventLogic()
        self.event_logic_func = EventLogic(None)
        self.filter_list: list[list] = []
        self.cctv_states = defaultdict(dict)
        self.command_queue: mp.Queue = mp.Queue(maxsize=30)
        self.test_type: int = -1  # 61: 안전대&안전고리 로직1, 62: 안전대&안전고리 로직2, 7: 보호구, 8: 월담, 9: 쓰러짐

    def get_model_data(self):
        """
        테스트용 데이터 추출
        [
            {'class_id': 0, 'confidence': 0.78, 'bbox': [283, 383, 334, 490]},
            {'class_id': 0, 'confidence': 0.77, 'bbox': [37, 401, 65, 576]},
            {'class_id': 2, 'confidence': 0.74, 'bbox': [371, 445, 439, 527]},
            {'class_id': 2, 'confidence': 0.65, 'bbox': [508, 442, 588, 524]},
            {'class_id': 2, 'confidence': 0.47, 'bbox': [437, 485, 474, 507]},
            {'class_id': 2, 'confidence': 0.4,  'bbox': [438, 498, 503, 515]},
            {'class_id': 2, 'confidence': 0.35, 'bbox': [89, 468, 160, 538]}
        ]
        """
        detections = []
        model = YOLO("yolov8s.pt", task="detect")
        img = cv2.imread("/home/rist/rist-ai-cctv-2025-2nd/img/2025-06-23/20250623_182938_CCTV 2.jpg")
        results = model(img)
        for result in results:
            if result.boxes is not None:
                for cls_id, conf, bbox in zip(result.boxes.cls, result.boxes.conf, result.boxes.xyxy):
                    cls_id = int(cls_id)
                    confidence = round(float(conf), 2)
                    bbox = [round(coord) for coord in bbox.tolist()]
                    detections.append({
                        "class_id": cls_id,
                        "confidence": confidence,
                        "bbox": bbox
                    })
        console.log(f"모델 데이터: {detections}")

    def call_event_function(self, func_name, *args, **kwargs):
        """동적으로 이벤트 함수를 호출합니다."""
        try:
            if hasattr(self.event_logic_func, func_name):
                event_func = getattr(self.event_logic_func, func_name)
                result = event_func(*args, **kwargs)
                # console.log(f"Called {func_name} with result: {result}")
                return result
            else:
                print(f"Function {func_name} not found in EventLogic class")
                return None
        except Exception as e:
            print(f"Error calling function {func_name}: {e}")
            return None

    def test_single_mapping_event_logic(self, cctv_name: str = "CCTV 1"):
        console.log("=== 단일 CCTV 이벤트 로직 매핑 테스트 ===")
        result = self.event_logic.mapping_event_logic(cctv_name)
        console.log(f"CCTV에 등록 된 이벤트 로직: {result}")
        return result

    def test_multiple_mapping_event_logic(self, start: int, end: int):
        console.log("=== 다중 CCTV 이벤트 로직 매핑 테스트 ===")
        cctv_list = []
        for i in range(start, end + 1):
            cctv_list.append(f"CCTV {i}")
        for cctv in cctv_list:
            logic = self.event_logic.mapping_event_logic(cctv)
            console.log(f"[{cctv}]: {logic}")

    def test_get_method_parameter(self, method_name: str):
        console.log("=== 메서드 파라미터 조회 테스트 ===")
        method = getattr(self.event_logic_func, method_name, None)
        parameter_list = [] # 파라미터 목록
        input_parameter_length = 0 # 입력 파라미터 개수

        # 메소드 검사
        if method is not None and inspect.ismethod(method):
            sig = inspect.signature(method)
            for param in sig.parameters.values():
                if param.default == inspect._empty:
                    parameter_list.append((param.name, param.annotation))

        # 입력 파라미터 수 검사
        input_parameter_length = len(parameter_list)
        if input_parameter_length == 0:
            console.log(f"이벤트 로직 메서드 '{method_name}'에 파라미터가 없습니다.")
        
        console.log(f"이벤트 로직 메서드 '{method_name}'의 파라미터 목록: {parameter_list}")
        return parameter_list
        
    def test_universal_dynamic_event(self, cctv_name: str = "CCTV 1", detection_data: List[dict] = None):
        frame_buffer = deque(maxlen=10)
        for i in range(10):
            frame_buffer.append((None, None))
        # return self._handle_sequential_detection(detection_data, "flash_suit", cctv_name, "RIGHT", 0, frame_buffer)

        result = False
        if self.test_type == 0:
            func_name = "safebelt3"
            result = self.call_event_function(func_name, detection_data, 0, 1, 2)
        else: 
            func_name = "safebelt4"
            result = self.call_event_function(func_name, detection_data, 0, 1)

        return result
    
    def _handle_sequential_detection(self, detection_data: List[dict], logic: str, cctv_name: str, direction_str: str = "", event_index: int = 0, frame_buffer: deque = None):
        """
        연속 프레임 기반의 지적확인 로직을 세션 기반으로 관리합니다.

        이 함수는 각 사람(person)별로 세션을 생성하고 추적하여,
        1. 지정된 구역에 들어왔는지 확인
        2. 구역 내에서 지적확인 행동을 수행했는지 기록
        3. 구역을 벗어났을 때, 설정된 이동 방향 규칙과 행동 수행 여부에 따라 최종 결과를 판정합니다.

        Args:
            detection_data (List[dict]): 현재 프레임의 객체 탐지 데이터.
            logic (str): 실행할 세부 로직 이름 (예: "jiguk1", "jiguk2").
            cctv_name (str): 현재 CCTV의 이름.
            direction_str (str): DB에 설정된 기준 이동 방향 (예: "LEFT", "RIGHT", "UP", "DOWN").
        """
        # console.log(detection_data)

        # 1. 상태 초기화 및 현재 프레임 분석
        # CCTV별 상태 초기화 (per-person sessions 지원)
        if cctv_name not in self.cctv_states:
            self.cctv_states[cctv_name] = {
                'person_sessions': {},  # person_id -> session_dict
                'jiguk_direction': direction_str,
                'cooldown_until': {},  # track_id -> timestamp
            }
        
        state = self.cctv_states[cctv_name]
        person_sessions = state['person_sessions']
        cooldown_expiry_time_by_person = state['cooldown_until']
        now = time.time()

        # event_logic_func.py의 함수 호출하여 현재 프레임 분석
        if hasattr(self.event_logic_func, logic):
            frame_result: dict = self.event_logic.call_event_function(logic, detection_data)
            if not frame_result:
                return False
            
            person_ids = set(frame_result.get('person_ids', []))
            site_entered_person_ids = set(frame_result.get('site_entered_person_ids', []))
            person_jiguk_not_detected = frame_result.get('person_jiguk_not_detected', {})
            
            # console.log(frame_result)
            # console.log(detection_data)

            if logic.startswith("jiguk1"):
                # 1. 새 세션 시작: 새로 진입한 사람 ID에 대해 세션 생성
                for person_id in site_entered_person_ids:
                    if person_id not in person_sessions:
                        session_id = f"{cctv_name}_{person_id}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}"
                        person_sessions[person_id] = JigukSessionData(
                            event_index=event_index,
                            session_id=session_id,
                            start_time=time.time(),
                            jiguk_check_deque=deque(maxlen=JIGUK_BUFFER_SIZE),
                            jiguk_performed=False,
                            consecutive_no_intersection=0,
                        )
                        # console.log(f"세션 시작 - CCTV: {cctv_name}, Person ID: {person_id}", style="bold green")
                
                # 2. 활성 세션 업데이트 및 종료 체크
                to_remove = []
                for person_id, session in list(person_sessions.items()):
                    session: JigukSessionData
                    if person_id in person_ids:
                        # 세션 유지: jiguk 상태 업데이트 (미검출 여부 추가)
                        if person_id in site_entered_person_ids:  # 아직 개소 안에 있음 (IoU > 0)
                            jiguk_not_detected = person_jiguk_not_detected.get(person_id, True)  # default 미검출
                            session.jiguk_check_deque.append(jiguk_not_detected)
                            if not jiguk_not_detected:
                                session.jiguk_performed = True
                            session.consecutive_no_intersection = 0  # 리셋
                        else:
                            # IoU == 0: 나간 것으로 간주, consecutive 증가
                            session.consecutive_no_intersection += 1
                    else:
                        # 사람 ID 자체가 검출되지 않음 (가려짐 등): consecutive 증가 (안전하게 종료 유예)
                        session.consecutive_no_intersection += 1

                    # 종료 조건: consecutive > 1 (짧은 노이즈 무시)
                    if session.consecutive_no_intersection > 1:
                        session.end_time = time.time()
                        jiguk_performed = session.jiguk_performed
                        status_label = "지적확인_실시" if jiguk_performed else "지적확인_미실시"
                        font_color = "bold green" if jiguk_performed else "bold yellow"
                        self.command_queue.put({
                            "type": MessageType.RECORD,
                            "cctv_name": cctv_name,
                            "status_label": status_label,
                            "session": session,
                        })
                        console.log(f"[{cctv_name}] [사람 ID: {person_id}] {status_label}", style=font_color)
                        to_remove.append(person_id)
                
                # 종료된 세션 제거
                for person_id in to_remove:
                    del person_sessions[person_id]

            elif logic.startswith("jiguk2"):
                # TODO: 지적확인 로직2 처리
                """
                1) 지적확인 장소에 n초 이상 있는지 확인 → n초 설정 시간이상 머무를시 →영상 저장 안함 → 같은 ID는 재검출 안함 n초 설정 이내 지적확인 장소 밖으로 나갈시 아래 로직 실행
                2) 로직(방향성 판단) 실행
                - 로직(방향성 판단)이 설정한 조건과 다를시 영상 저장 안함  → UI 화면에 알람 발생X
                - 로직(방향성 판단)이 설정한 조건과 동일시 → 지적확인 프레임 확인 → UI 화면에 알람 발생X  → 영상 저장을 “지적확인 실시” 파일명 저장
                - 로직(방향성 판단)이 설정한 조건과 동일시 → 지적확인 프레임 미확인 → UI 화면에 2초간 알람 발생O → 영상 저장을 “지적확인 미실시” 파일명 저장
                """
                # 1. 새 세션 시작: 새로 진입한 사람 ID에 대해 세션 생성
                for person_id in site_entered_person_ids:

                    # 쿨다운이면 신규 세션 생성 금지
                    if cooldown_expiry_time_by_person.get(person_id, 0) > now:
                        continue
                    
                    if person_id not in person_sessions:
                        # detection_data에서 person_id에 해당하는 사람의 bbox 찾기
                        person_data = next((data for data in detection_data if data['track_id'] == person_id and data['class_id'] == 0), None)
                        if person_data:
                            # 중심점 계산: (x_min + x_max) / 2, (y_min + y_max) / 2
                            bbox = person_data['bbox']  # [x_min, y_min, x_max, y_max]
                            initial_center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

                            # 세션 생성
                            session_id = f"{cctv_name}_{person_id}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}"
                            person_sessions[person_id] = JigukSessionData(
                                event_index=event_index,
                                session_id=session_id,
                                start_time=now,
                                jiguk_check_deque=deque(maxlen=JIGUK_BUFFER_SIZE),
                                jiguk_performed=False,
                                consecutive_no_intersection=0,
                                jiguk_direction=direction_str,
                                initial_center=initial_center,          # 초기 중심점 저장
                                final_center=None,                      # 종료 시 중심점 저장
                                last_time_in_space=now,
                                last_seen_time=now,
                                time_when_left_space=None,
                                current_state=SessionState.IN           # IN | OUT_PENDING
                            )
                            console.log(f"세션 시작 - CCTV: {cctv_name}, Person ID: {person_id}, 초기 중심점: {initial_center}, 방향: {direction_str}", style="bold green")

                # 2. 활성 세션 업데이트 및 종료 체크
                to_remove = []
                for person_id, session in list(person_sessions.items()):
                    session: JigukSessionData

                    # 세션 상태 복귀/유지
                    session.last_seen_time = now
                    in_zone = (person_id in site_entered_person_ids)
                    if in_zone:
                        # 상태 복귀/유지
                        session.current_state = "IN"
                        session.time_when_left_space = None
                        session.last_time_in_space = now
                        session.consecutive_no_intersection = 0
                        session.yolo_result_on_exit = frame_buffer[-1][1] 

                        # jiguk 상태/최신 중심점 업데이트
                        jiguk_not_detected = person_jiguk_not_detected.get(person_id, True)
                        session.jiguk_check_deque.append(jiguk_not_detected)
                        if not jiguk_not_detected:
                            session.yolo_result_on_jiguk = session.yolo_result_on_exit
                            session.jiguk_performed = True
                        person_data = next((d for d in detection_data
                                            if d['track_id'] == person_id and d['class_id'] == 0), None)
                        if person_data:
                            x1, y1, x2, y2 = person_data['bbox']
                            session.final_center = ((x1 + x2) / 2, (y1 + y2) / 2)
                        continue

                    # === 개소 밖인 경우 ===
                    if session.current_state != SessionState.OUT_PENDING:
                        # 이탈 감지 시작 → 유예 타이머 시작
                        session.current_state = SessionState.OUT_PENDING
                        session.time_when_left_space = now

                    # 유예 시간 경과 여부 체크(시간 기반)
                    if session.last_time_in_space is not None and (now - session.last_time_in_space) >= LEAVE_GRACE_SEC:
                        # --- 종료 확정: 여기서 1회 방향 판정 ---
                        # (1) n초 이상 체류면 스킵 + 쿨다운
                        stay_duration_in_zone = (session.last_time_in_space - session.start_time) if session.last_time_in_space else 0.0
                        if stay_duration_in_zone >= MIN_DWELL_SEC:
                            cooldown_expiry_time_by_person[person_id] = now + COOLDOWN_SEC
                            to_remove.append(person_id)
                            continue

                        # (2) 방향 판정
                        is_direction_correct = False
                        session.direction_result_str = DirectionType.NONE.result_str
                        if session.initial_center and session.final_center:
                            dx = session.final_center[0] - session.initial_center[0]
                            dy = session.final_center[1] - session.initial_center[1]
                            if abs(dx) + abs(dy) >= MIN_MOVE_PX:
                                if abs(dx) > abs(dy):
                                    detected = DirectionType.RIGHT if dx > 0 else DirectionType.LEFT
                                else:
                                    detected = DirectionType.DOWN if dy > 0 else DirectionType.UP
                                session.direction_result_str = detected.result_str
                                is_direction_correct = (detected.config_str == session.jiguk_direction)

                        # (3) 결과 기록/로깅 (여기 ‘한 번’만 출력)
                        session.current_state = SessionState.OUT
                        session.end_time = now
                        if is_direction_correct:
                            status_label = "지적확인_실시" if session.jiguk_performed else "지적확인_미실시"
                            font_color = "bold green" if session.jiguk_performed else "bold red"
                            if session.jiguk_performed:
                                yolo_result = session.yolo_result_on_jiguk
                            else:
                                yolo_result = session.yolo_result_on_exit

                            self.command_queue.put({
                                "type": MessageType.RECORD,
                                "cctv_name": cctv_name,
                                "status_label": status_label,
                                "session": session,
                                "yolo_result": yolo_result,
                            })
                            console.log(f"[{cctv_name}] [사람 ID: {person_id}] {status_label}, 이동방향: {session.direction_result_str} | 큐 1회 송신", style=font_color)
                        else:
                            console.log(f"[{cctv_name}] [사람 ID: {person_id}] 방향 조건 불충족, 이동방향: {session.direction_result_str}", style="bold yellow")

                        # (4) 종료 후 재진입 쿨다운 부여
                        cooldown_expiry_time_by_person[person_id] = now + COOLDOWN_SEC
                        to_remove.append(person_id)

                # 종료된 세션 제거
                for person_id in to_remove:
                    person_sessions.pop(person_id, None)

            else:
                console.log(f"지원하지 않는 지적확인 로직: {logic}")
                return False

        return False
    
    def calculate_moving_vector(self):
        """
        직전 3 프레임의 detection_data를 기반으로 사람 객체의 이동 방향을 계산

        사람 객체 중심점: [(956, 540), (972, 540), (988, 540)]
        """
        MOVE_TYPE = ["up", "down", "left", "right"]
        moving_points = []
        for detection_data in self.moving_vector_deque:
            for obj in detection_data:
                if obj['class_id'] == 0:
                    x1, y1, x2, y2 = obj["bbox"]
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    person_center = (center_x, center_y)
            moving_points.append(person_center)

        p_array = np.array(moving_points, dtype=float)

        global_diff = p_array[-1] - p_array[0]
        global_norm = np.linalg.norm(global_diff)
        global_direction = global_diff / global_norm if global_norm != 0 else np.zeros(2)

        if global_direction[0] == 0 and global_direction[1] > 0:
            console.print(f"Moving direction: {MOVE_TYPE[0]}")
        elif global_direction[0] == 0 and global_direction[1] < 0:
            console.print(f"Moving direction: {MOVE_TYPE[1]}")
        elif global_direction[0] < 0 and global_direction[1] == 0:
            console.print(f"Moving direction: {MOVE_TYPE[2]}")
        elif global_direction[0] > 0 and global_direction[1] == 0:
            console.print(f"Moving direction: {MOVE_TYPE[3]}")

    def _preprocess_detection_data(self, detection_data, param_meta):
        """
        detection 데이터를 class_id별로 그룹화

        defaultdict(<class 'list'>, {
            0: [
            {'class_id': 0, 'confidence': 0.78, 'bbox': [283, 383, 334, 490]},
            {'class_id': 0, 'confidence': 0.77, 'bbox': [37, 401, 65, 576]}
            ],
            2: [
            {'class_id': 2, 'confidence': 0.74, 'bbox': [371, 445, 439, 527]},
            {'class_id': 2, 'confidence': 0.65, 'bbox': [508, 442, 588, 524]},
            {'class_id': 2, 'confidence': 0.47, 'bbox': [437, 485, 474, 507]},
            {'class_id': 2, 'confidence': 0.4,  'bbox': [438, 498, 503, 515]},
            {'class_id': 2, 'confidence': 0.35, 'bbox': [89, 468, 160, 538]}
            ]
        })
        """
        class_groups = defaultdict(list)
        for item in detection_data:
            class_id = item['class_id']
            class_groups[class_id].append(item)
        
        return class_groups
    
    def calculate_iou(self, boxA, boxB):
        """ 두 바운딩 박스의 IoU(Intersection over Union)를 계산합니다. """
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        unionArea = float(boxAArea + boxBArea - interArea)
        return interArea / unionArea if unionArea > 0 else 0

    def convert_csv_to_detection_data_with_sort(self, csv_data: str) -> dict:
        """
        CSV 데이터를 프레임별 detection_data로 변환하며,
        IoU 정렬 기반의 SORT 방식으로 track_id를 유지합니다.
        """
        data_io = io.StringIO(csv_data)
        df = pd.read_csv(data_io)
        
        all_frames_data = {}
        
        # --- 추적 로직을 위한 상태 변수 ---
        active_tracks = {}  # {track_id: {"bbox": bbox, "class_id": cid, "last_seen": frame_num}}
        next_track_id = 1
        IOU_THRESHOLD = 0.3  # IoU 임계값 (이전보다 낮춰서 매칭 확률을 높임)
        MAX_AGE = 5          # 트랙이 보이지 않아도 유지할 최대 프레임 수

        # 프레임 번호로 그룹화하여 순회
        for frame_num, frame_group in sorted(df.groupby('frame')):
            
            current_detections = []
            for _, row in frame_group.iterrows():
                current_detections.append({
                    "track_id": None,
                    "class_id": int(row['class']),
                    "confidence": float(row['confidence']),
                    "bbox": (int(row['x1']), int(row['y1']), int(row['x2']), int(row['y2']))
                })

            # --- SORT 기반 매칭 로직 ---
            
            # 1. 가능한 모든 매칭 쌍의 IoU 계산
            iou_matches = []
            for track_id, track_data in active_tracks.items():
                for i, det in enumerate(current_detections):
                    # 클래스가 다르면 건너뜀
                    if det['class_id'] != track_data['class_id']:
                        continue
                    
                    iou = self.calculate_iou(track_data['bbox'], det['bbox'])
                    if iou > IOU_THRESHOLD:
                        iou_matches.append((iou, track_id, i)) # (IoU, 트랙ID, 탐지객체 인덱스)
            
            # 2. IoU 값 기준으로 내림차순 정렬
            iou_matches.sort(key=lambda x: x[0], reverse=True)
            
            assigned_detections = set()
            assigned_tracks = set()

            # 3. 가장 IoU가 높은 순서대로 매칭
            for iou, track_id, det_idx in iou_matches:
                # 이미 매칭된 트랙이나 객체는 건너뜀
                if track_id in assigned_tracks or det_idx in assigned_detections:
                    continue
                
                # 매칭 확정
                current_detections[det_idx]['track_id'] = track_id
                current_detections[det_idx]["filter"] = True
                active_tracks[track_id]['bbox'] = current_detections[det_idx]['bbox']
                active_tracks[track_id]['last_seen'] = frame_num # 마지막으로 본 프레임 갱신
                
                assigned_tracks.add(track_id)
                assigned_detections.add(det_idx)

            # 4. 매칭되지 않은 객체는 새 트랙으로 등록
            for i, det in enumerate(current_detections):
                if i not in assigned_detections:
                    det['track_id'] = next_track_id
                    active_tracks[next_track_id] = {
                        'bbox': det['bbox'],
                        'class_id': det['class_id'],
                        'last_seen': frame_num
                    }
                    next_track_id += 1
            
            # 5. 오래된 트랙 제거
            inactive_tracks = []
            for track_id, track_data in active_tracks.items():
                if frame_num - track_data['last_seen'] > MAX_AGE:
                    inactive_tracks.append(track_id)
            
            for track_id in inactive_tracks:
                del active_tracks[track_id]

            all_frames_data[frame_num] = current_detections
                
        return all_frames_data

    def csv_test(self):
        csv_input = open("/home/skysys/rist-ai-cctv-2025-2nd/event_logic/data/jiguk_ok.csv", "r").read()
        detection_data_per_frame = self.convert_csv_to_detection_data_with_sort(csv_input)

        console.rule("동적 이벤트 테스트 (30fps 시뮬레이션)")
        
        for i, detections in enumerate(detection_data_per_frame.values()):
            self.event_logic.frame_buffer = deque([ (None, None) ], maxlen=1)
            result = self.test_universal_dynamic_event(detection_data=detections)
            console.log(f"동적 이벤트 테스트 결과 (프레임 {i}): {result}")
            time.sleep(1 / 30)
            
        console.rule("이벤트 테스트 완료")
        
        # 2. 루프 종료 후, 남아있는 세션을 처리하기 위한 추가 실행
        console.rule("세션 종료 처리 시뮬레이션")
        grace_period_frames = int(30 * LEAVE_GRACE_SEC * 2) 
        for i in range(grace_period_frames):
            result = self.test_universal_dynamic_event(detection_data=[])
            if result:
                 console.log(f"세션 종료 처리 중 이벤트 발생 (추가 프레임 {i}): {result}")
            time.sleep(1 / 30)

    def _create_danger_detection(self, res: Results, class_filter: set[int]) -> list[dict]:
        """
        results_by_model: { model_name: Results }
        class_filters:    { model_name: {class_index, ...} }  # 없으면 전체 허용

        # 개구부, 안전벨트, 월담, 쓰러짐 감지
        {0: 'person', 1: 'lift', 2: 'forklift', 3: 'gagubu', 4: 'safebelt', 5: 'hook', 6: 'connect_hook', 7: 'flash_suit', 8: 'waldam', 9: 'open_door', 10: 'flash_fire', 11: 'falldown'}

        # 보호구 감지
        {0: 'person', 1: 'lift', 2: 'flash_fire', 3: 'gagubu', 4: 'safebelt', 5: 'hook', 6: 'connect_hook', 7: 'flash_suit', 8: 'waldam', 9: 'open_door'}


        """
        
        detections: list[dict] = []

        allow: set[int] | None = class_filter
        boxes = getattr(res, "boxes", None)

        # to numpy
        xyxy = boxes.xyxy.detach().cpu().numpy() if boxes.xyxy is not None else None
        cls  = boxes.cls.detach().cpu().numpy().astype(int) if boxes.cls is not None else None
        conf = boxes.conf.detach().cpu().numpy() if boxes.conf is not None else None
        n = xyxy.shape[0]

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
            track_id = int(track_id) if track_id >= 0 else None

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
    
    def run(self):
        class_filter: set[int] = set()
        model: YOLO = None
        cap = None
        frame_count = 0

        try:


            class_filter = {0, 1, 2} # 사람, 트럭, 안전고리
            model = YOLO("/home/skysys/rist_model_test/SB3/best.pt", task="detect")
            cap = cv2.VideoCapture("/home/skysys/rist_model_test/SB3/SB_4.mp4")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1

                if frame_count % 3 != 0:
                    continue
                else:
                    results = model.track(frame, verbose=False, persist=True, tracker=paths.TRACKER_LOCATION)
                    detections = self._create_danger_detection(results[0], class_filter)
                    console.log(detections)
                    ret = self.test_universal_dynamic_event(detection_data=detections)
                    if ret:
                        if self.test_type == 0:
                            console.log("[bold red]🚨 트럭 안전벨트 미착용 알람![/bold red]")
                        else:
                            console.log("[bold red]🚨 트럭 상부 사람 감지 알람![/bold red]")
                    else:
                        if self.test_type == 0:
                            console.log("[bold green]트럭 안전벨트 착용 정상[/bold green]")
                        else:
                            console.log("[bold green]트럭 상부 사람 없음 정상[/bold green]")
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

        finally:
            cap.release()


if __name__ == "__main__":
    test = TestEventLogic()
    test.test_type = 1
    test.run()
