import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csv
import inspect
import time
import numpy as np
import multiprocessing as mp
from typing import Tuple
from collections import defaultdict, deque
from rich.console import Console
from rich.traceback import install
from setting import paths
from setting.use_qsetting import Setting
from db.db_cctv_list import DbCctvList
from db.db_logic_list import DbLogicList
from event_logic.event_logic_func import EventLogic
from widget.video_process_pipeline.video_config import setup_logger, ConfigManager, MessageType, JigukSessionData, DirectionType, SessionState, VideoConfig


install()
console = Console()
INI_CONFIG = ConfigManager()

class SetupEventLogic:
    def __init__(self, command_queue: mp.Queue = None):
        """초기화 시 설정 파일을 확인하고 생성합니다."""
        self.logger = setup_logger("event_logic")
        self.command_queue: mp.Queue = command_queue  # 명령 큐 초기화
        self.event_logic = EventLogic(event_data=None) # EventLogic 인스턴스 생성 (event_data는 나중에 설정)
        self.cctv_states = defaultdict(dict)  # CCTV별 상태 관리
        self.frame_buffer: deque = None # 프레임 버퍼 초기화 (2025-08-14 현재 미사용 변수)
        self.event_mapper: dict[int, Tuple[str, str]] = defaultdict(tuple)
        self.config: VideoConfig = None
        self.is_debug: bool = True

    def set_config(self, config: VideoConfig):
        self.config = config

    def mapping_event_logic(self, camera_name: str = "CCTV 4", event_index: int = 0):
        """CCTV 이름을 기준으로 할당된 이벤트 로직 검색"""
        logic_dict: dict = INI_CONFIG.logic_dict
        if not logic_dict:
            console.log("No logic list found in settings.")
            return
        
        cctv_list = DbCctvList().select(camera_name=camera_name)
        event_name_list = []
        for cctv in cctv_list:
            event_name_str: str = cctv.unsafe_event
            event_name_list = event_name_str.split(",")


        # DB에서 이벤트 로직 조회
        event_name = event_name_list[event_index].strip()
        logic_result = DbLogicList().select(logic_name=event_name)
        if not logic_result:
            self.logger.info(f"CCTV: {camera_name}, Event Logic: {event_name} not found in DB")
            return
        
        # 이벤트 로직에서 함수명 조회
        func_name = ""
        for event in logic_result[0].logicListData:
            event_name = event.get("name")
            try:
                # 설정에서 함수명 매핑 확인
                func_name = logic_dict.get(event_name)
            except Exception as e:
                pass

        # jiguk_direction 설정
        jiguk_direction_value  = logic_result[0].jiguk_direction if hasattr(logic_result[0], "jiguk_direction") else None
        direction_enum_member = DirectionType.from_db(jiguk_direction_value)
        direction = direction_enum_member.config_str

        self.event_mapper[event_index] = (func_name, direction)

    def get_logic_list(self, func_name, *args, **kwargs):
        # getattr을 사용하여 문자열로 된 함수명을 실제 함수로 변환
        if hasattr(self.event_logic, func_name):
            console.log(f"Function {func_name} is ready to be called")
            
            # 함수에 따라 다른 인수를 전달하는 예시
            result = self.call_event_function(
                func_name, *args, **kwargs
            )      
            return result                
        else:
            console.log(f"Function {func_name} not found in EventLogic class")
            
    def call_event_function(self, func_name, *args, **kwargs):
        """동적으로 이벤트 함수를 호출합니다."""
        try:
            if hasattr(self.event_logic, func_name):
                event_func = getattr(self.event_logic, func_name)
                result = event_func(*args, **kwargs)
                # console.log(f"Called {func_name} with result: {result}")
                return result
            else:
                print(f"Function {func_name} not found in EventLogic class")
                return None
        except Exception as e:
            self.logger.info(f"Error calling function {func_name}: {e}")
            return None

    def get_method_parameter(self, method_name: str):
        try:
            method = getattr(self.event_logic, method_name, None)
        except:
            return []
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
            print(f'이벤트 로직 메서드 "{method_name}"에 파라미터가 없습니다.')
        
        # print(f"이벤트 로직 메서드 "{method_name}"의 파라미터 목록: {parameter_list}")
        return parameter_list

    def universal_dynamic_event_process(self, cctv_name: str = "CCTV 1", event_index: int = 0,
                                    detection_data: list[dict] = [], frame_buffer: deque[np.ndarray] = None,
                                    filter_dict: dict = {}) -> bool | int:
        """
        CCTV별 이벤트 로직을 동적으로 실행하는 범용 이벤트 처리 함수
        
        CCTV 이름을 기준으로 해당 CCTV에 할당된 이벤트 로직을 자동으로 매핑하고,
        함수의 파라미터 타입을 분석하여 적절한 처리 방식을 선택한 후 동적으로 실행합니다.
        
        처리 방식:
        1. Label 기반 탐지: str 파라미터만 있는 경우
        - 특정 class_id(객체 클래스)의 존재 여부만 확인
        - 예: detect_fire(label: str) -> ex) "fire" 클래스 탐지 시 True
        
        2. Bbox 기반 탐지: tuple 파라미터만 있는 경우  
        - 서로 다른 class_id 간의 bbox 조합을 생성하여 관계 분석
        - class_id 0(사람)을 기준으로 다른 객체들과의 조합 생성
        - 예: is_bbox_close(bbox_1: tuple, bbox_2: tuple) -> 두 객체 간 거리 분석
        
        Args:
            cctv_name (str, optional): 이벤트 로직을 조회할 CCTV 이름. Defaults to "CCTV 1".
            detection_data (List[dict], optional): 객체 탐지 결과 데이터. Defaults to [].
                각 dict는 다음 키를 포함해야 함:
                - "class_id" (int): 객체 클래스 ID (YOLO 클래스)
                - "confidence" (float): 탐지 신뢰도 (0.0~1.0)
                - "bbox" (List[int]): 바운딩 박스 좌표 [x1, y1, x2, y2]
        
        Returns:
            bool: 위험 상황 탐지 여부
                - True: 이벤트 조건을 만족하는 상황이 탐지됨
                - False: 이벤트 조건을 만족하지 않거나 탐지 실패
        """

        self.frame_buffer: deque = frame_buffer
        current_cctv_fps: float = self.config.cctv_fps # CCTV FPS 정보 (float)
        current_event_list: list[dict] = self.config.event
        current_skip_frame: int = max(current_event_list[event_index].get("skip_frame", 1), 1)
        current_detection_fps: int = int(current_cctv_fps / current_skip_frame)
        
        if not self.event_mapper[event_index]:
            self.mapping_event_logic(cctv_name, event_index)
        
        logic, direction = self.event_mapper[event_index]

        param_meta: list[tuple] = self.get_method_parameter(logic)
        if not param_meta:
            return False
        
        tuple_values = [name for name, cls in param_meta if cls == tuple]
        str_values = [name for name, cls in param_meta if cls == str]

        # 연속 프레임 검증이 필요한 로직인지 확인
        is_sequential_logic = logic.startswith("jiguk") or logic == "bulti" or logic == "detect_collision"

        if is_sequential_logic:
            # 불티비산(훈소) 감지
            if logic == "bulti":
                fire_spark_class_id = 1
                smoke_class_id = 0
                return self.call_event_function(
                    logic, detection_data,
                    fire_spark_class_id=fire_spark_class_id,
                    smoke_class_id=smoke_class_id,
                    extend_pixel=INI_CONFIG.bulti_config.roi_extend_pixel,
                    roi_duration_time=INI_CONFIG.bulti_config.roi_maintain_time
                )
            
            # 접근감지
            elif logic == "detect_collision":
                target_class_id = 2
                if current_event_list:
                    """
                    current_event_list = [
                        {
                            "name": "09_5_개구부 진입 감지",
                            "skip_frame": 2,
                            "input_img_size": "640,640",
                            "models": [
                                {"type": "AI", "name": "05_gagubu", "class_name": "person", "class_index": 0},
                                {"type": "AI", "name": "05_gagubu", "class_name": "gagubu", "class_index": 3},
                                {"type": "algorithm", "name": "접근감지", "class_name": None, "class_index": None}
                            ],
                            "risk_level": 2 
                        }
                    ]
                    """
                    for model_info in current_event_list[event_index].get("models", []):
                        """
                        model_info = {"type": "AI", "name": "05_gagubu", "class_name": "person", "class_index": 0}
                        model_info = {"type": "AI", "name": "05_gagubu", "class_name": "gagubu", "class_index": 3}

                        model_info는 current_event_list에서 models의 값을 하나씩 가져온다.
                        이 때, model_info의 class_name이 "person"이 아닌 첫번째 class_index를 target_class_id로 설정한다.

                        접근 감지 로직의 경우 사람 객체와 다른 객체 간의 충돌을 감지하는 로직이므로, 로직을 설정할 때 사람 객체와 타겟 객체만 필터에 추가된다.
                        즉, model_info의 class_name이 "person"이 아닌 객체는 타겟 객체로 간주할 수 있다.

                        """
                        if model_info.get("class_name") not in ["person", "worker"]:
                            target_class_id = model_info.get("class_index")
                            break
                return self.call_event_function(
                    logic, detection_data,
                    target_class_id=target_class_id,
                    extend_pixel=INI_CONFIG.collision_config.roi_extend_pixel,
                    max_window_frames_len=INI_CONFIG.collision_config.max_window_frames,
                    min_collision_frames=INI_CONFIG.collision_config.min_collision_frames
                )

            # 지적확인
            else:
                return self._handle_sequential_detection(detection_data, logic, cctv_name, direction, event_index, frame_buffer)
            
        # 안전대&안전벨트 로직 1
        elif logic == "safebelt1":
            person_class_id = 0
            safebelt_class_id = 4
            hook_class_id = 5
            hook_connection_class_id = 6
            actual_deque_size = (INI_CONFIG.safebelt_config.logic_1_detect_time * current_detection_fps)
            return self.call_event_function(
                logic, detection_data,
                person_class_id=person_class_id,
                safebelt_class_id=safebelt_class_id,
                hook_class_id=hook_class_id,
                hook_connection_class_id=hook_connection_class_id,
                max_deque_size=actual_deque_size
            )
        
        # 안전대&안전벨트 로직 2
        elif logic == "safebelt2":
            person_class_id = 0
            safebelt_class_id = 4
            hook_class_id = 5
            open_door_class_id = 9
            roi_extend_pixel = INI_CONFIG.safebelt_config.roi_extend_pixel
            actual_deque_size = (INI_CONFIG.safebelt_config.logic_2_detect_time * current_detection_fps)
            return self.call_event_function(
                logic, detection_data,
                person_class_id=person_class_id,
                safebelt_class_id=safebelt_class_id,
                hook_class_id=hook_class_id,
                open_door_class_id=open_door_class_id,
                roi_extend_pixel=roi_extend_pixel,
                max_deque_size=actual_deque_size
            )
        
        # 보호구 감지
        elif logic == "flash_suit":
            person_class_id = 0
            flash_fire_class_id = 2
            flash_suit_class_id = 7
            roi_extend_pixel = INI_CONFIG.flash_suit_config.roi_extend_pixel
            actual_deque_size = (INI_CONFIG.flash_suit_config.detect_time * current_detection_fps)
            return self.call_event_function(
                logic, detection_data,
                person_class_id=person_class_id,
                flash_fire_class_id=flash_fire_class_id,
                flash_suit_class_id=flash_suit_class_id,
                roi_extend_pixel=roi_extend_pixel,
                min_deque_size=actual_deque_size
            )
        
        # 월담 감지
        elif logic == "waldam":
            person_class_id = 0
            space_class_id = 1
            waldam_class_id = 2
            return self.call_event_function(
                logic, detection_data,
                person_class_id=person_class_id,
                space_class_id=space_class_id,
                waldam_class_id=waldam_class_id,
            )
        
        # 쓰러짐 감지
        elif logic == "falldown":
            person_class_id = 0
            falldown_class_id = 9
            return self.call_event_function(
                logic, detection_data,
                person_class_id=person_class_id,
                target_class_id=falldown_class_id,
            )
        
        elif logic == "person_count":
            person_class_id = 0
            return self.call_event_function(
                logic, detection_data,
                person_class_id=person_class_id,
            )
        
        elif str_values and not tuple_values:
            return self._handle_label_based_detection(detection_data, logic, param_meta, str_values)
        
        elif tuple_values and not str_values:
            return self._handle_bbox_based_detection(detection_data, logic, param_meta)
        
        else:
            return False

    def _handle_sequential_detection(self, detection_data: list[dict], logic: str, cctv_name: str, direction_str: str = "", event_index: int = 0, frame_buffer: deque = None):
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
        # 1. 상태 초기화 및 현재 프레임 분석
        # CCTV별 상태 초기화 (per-person sessions 지원)
        if cctv_name not in self.cctv_states:
            self.cctv_states[cctv_name] = {
                "person_sessions": {},  # person_id -> session_dict
                "jiguk_direction": direction_str,
                "cooldown_until": {},  # track_id -> timestamp
            }
        
        state = self.cctv_states[cctv_name]
        person_sessions = state["person_sessions"]
        cooldown_expiry_time_by_person = state["cooldown_until"]
        now = time.time()

        # event_logic_func.py의 함수 호출하여 현재 프레임 분석
        if hasattr(self.event_logic, logic):
            frame_result: dict = self.call_event_function(logic, detection_data)
            if not frame_result:
                return False
            
            person_ids = set(frame_result.get("person_ids", []))
            site_entered_person_ids = set(frame_result.get("site_entered_person_ids", []))
            person_jiguk_not_detected = frame_result.get("person_jiguk_not_detected", {})
            
            if logic.startswith("jiguk1"):
                # 1. 새 세션 시작: 새로 진입한 사람 ID에 대해 세션 생성
                for person_id in site_entered_person_ids:
                    if person_id not in person_sessions:
                        # 세션 생성
                        session_id = f"{cctv_name}_id_{person_id}_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}"
                        person_sessions[person_id] = JigukSessionData(
                            event_index=event_index,
                            session_id=session_id,
                            start_time=time.time(),
                            jiguk_check_deque=deque(maxlen=INI_CONFIG.global_config.jiguk_buffer_size),
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
                                session.yolo_result_on_jiguk = frame_buffer[-1][1]
                                session.jiguk_performed = True
                            session.consecutive_no_intersection = 0  # 리셋
                        else:
                            # IoU == 0: 나간 것으로 간주, consecutive 증가
                            session.consecutive_no_intersection += 1
                    else:
                        # 사람 ID 자체가 검출되지 않음 (가려짐 등): consecutive 증가 (안전하게 종료 유예)
                        session.consecutive_no_intersection += 1

                    # 종료 조건: consecutive > 2 (짧은 노이즈 무시)
                    if session.consecutive_no_intersection > 2:
                        session.yolo_result_on_exit = frame_buffer[-1][1] 
                        session.end_time = time.time()
                        jiguk_performed = session.jiguk_performed
                        if jiguk_performed:
                            yolo_result = session.yolo_result_on_jiguk
                        else:
                            yolo_result = session.yolo_result_on_exit
                        status_label = "지적확인_실시" if jiguk_performed else "지적확인_미실시"
                        font_color = "bold green" if jiguk_performed else "bold yellow"
                        self.command_queue.put({
                            "type": MessageType.RECORD,
                            "cctv_name": cctv_name,
                            "status_label": status_label,
                            "session": session,
                            "yolo_result": yolo_result,
                        })
                        # console.log(f"[{cctv_name}] [사람 ID: {person_id}] {status_label}", style=font_color)
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
                        person_data = next((data for data in detection_data if data["track_id"] == person_id and data["class_id"] == 0), None)
                        if person_data:
                            # 중심점 계산: (x_min + x_max) / 2, (y_min + y_max) / 2
                            bbox = person_data["bbox"]  # [x_min, y_min, x_max, y_max]
                            initial_center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

                            # 세션 생성
                            session_id = f"{cctv_name}_id_{person_id}_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}"
                            person_sessions[person_id] = JigukSessionData(
                                event_index=event_index,
                                session_id=session_id,
                                start_time=now,
                                jiguk_check_deque=deque(maxlen=INI_CONFIG.global_config.jiguk_buffer_size),
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
                            # console.log(f"세션 시작 - CCTV: {cctv_name}, Person ID: {person_id}, 초기 중심점: {initial_center}, 방향: {direction_str}", style="bold green")

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
                                            if d["track_id"] == person_id and d["class_id"] == 0), None)
                        if person_data:
                            x1, y1, x2, y2 = person_data["bbox"]
                            session.final_center = ((x1 + x2) / 2, (y1 + y2) / 2)
                        continue

                    # === 개소 밖인 경우 ===
                    if session.current_state != SessionState.OUT_PENDING:
                        # 이탈 감지 시작 → 유예 타이머 시작
                        session.current_state = SessionState.OUT_PENDING
                        session.time_when_left_space = now

                    # 유예 시간 경과 여부 체크(시간 기반)
                    if session.last_time_in_space is not None and (now - session.last_time_in_space) >= INI_CONFIG.session_config.leave_grace_sec:
                        # --- 종료 확정: 여기서 1회 방향 판정 ---
                        # (1) n초 이상 체류면 스킵 + 쿨다운
                        stay_duration_in_zone = (session.last_time_in_space - session.start_time) if session.last_time_in_space else 0.0
                        if stay_duration_in_zone >= INI_CONFIG.session_config.min_dwell_sec:
                            cooldown_expiry_time_by_person[person_id] = now + INI_CONFIG.session_config.cooldown_sec
                            to_remove.append(person_id)
                            continue

                        # (2) 방향 판정
                        is_direction_correct = False
                        session.direction_result_str = DirectionType.NONE.result_str
                        if session.initial_center and session.final_center:
                            dx = session.final_center[0] - session.initial_center[0]
                            dy = session.final_center[1] - session.initial_center[1]
                            if abs(dx) + abs(dy) >= INI_CONFIG.session_config.min_move_px:
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
                            # console.log(f"[{cctv_name}] [사람 ID: {person_id}] {status_label}, 이동방향: {session.direction_result_str}", style=font_color)
                        else:
                            # console.log(f"[{cctv_name}] [사람 ID: {person_id}] 방향 조건 불충족, 이동방향: {session.direction_result_str}", style="bold yellow")
                            pass

                        # (4) 종료 후 재진입 쿨다운 부여
                        cooldown_expiry_time_by_person[person_id] = now + INI_CONFIG.session_config.cooldown_sec
                        to_remove.append(person_id)

                # 종료된 세션 제거
                for person_id in to_remove:
                    person_sessions.pop(person_id, None)

            else:
                console.log(f"지원하지 않는 지적확인 로직: {logic}")
                return False

        return False
    
    def _handle_label_based_detection(self, detection_data, logic, param_meta, str_values):
        """
        label 파라미터가 있는 경우: 특정 class_id 존재 여부만 확인
        
        2025-06-24
        현재 미완성
        class_label을 Triton에 등록된 모델의 metadata로부터 가져와야 함
        지금은 하드코딩 된 상태
        """
        # class_id를 label로 매핑하는 사전 (YOLO 클래스 매핑) <-- 이 부분 나중에 Triton 모델의 metadata로부터 동적으로 가져와야 함
        class_id_to_label = {
            0: "person",
            1: "bicycle", 
            2: "car",
            3: "fire",  # 예시
        }
        
        # detection_data에서 사용 가능한 class_id들 추출
        detected_class_ids = set(item["class_id"] for item in detection_data)
        
        # 각 탐지된 class_id에 대해 함수 호출
        for class_id in detected_class_ids:
            if class_id in class_id_to_label:
                label = class_id_to_label[class_id]
                
                # label 파라미터만 사용하여 함수 호출
                kwargs = {}
                for param_name, param_type in param_meta:
                    if param_type == str:  # label 파라미터
                        kwargs[param_name] = label
                
                result = self.call_event_function(logic, **kwargs)
                
                if result:  # 하나라도 True면 즉시 반환
                    return True
        
        return False
    
    def _handle_bbox_based_detection(self, detection_data: list, logic: str, param_meta: list[tuple]):
        """bbox 파라미터만 있는 경우: 기존 조합 기반 탐지"""
        processed_data = self._preprocess_detection_data(detection_data, param_meta)
        combinations_generator = self._generate_combinations(processed_data, len(param_meta))

        # 동적 함수 호출
        # 지적확인 로직의 경우, 모든 조합이 True여야만 True 반환
        if logic.startswith("jiguk"):
            if not combinations_generator:
                return False
            else:
                all_results = []
                # console.log(f"{logic} 조합 생성")
                for combo in combinations_generator:
                    kwargs = {name: value for (name, _), value in zip(param_meta, combo)}
                    result = self.call_event_function(logic, **kwargs)
                    # console.log(f"조합: {kwargs}, 결과: {result}")
                    all_results.append(result)
                result = all(result is True for result in all_results)
                # console.log(f"모든 조합 결과: {result}")
                return result
        else:
            # 일반적인 bbox 기반 탐지의 경우, 하나라도 True면 즉시 반환
            for combo in combinations_generator:
                kwargs = {name: value for (name, _), value in zip(param_meta, combo)}
                result = self.call_event_function(logic, **kwargs)
                if result:
                    return True
        return False
        
    def _preprocess_detection_data(self, detection_data, param_meta):
        """detection 데이터를 class_id별로 그룹화"""
        class_groups = defaultdict(list)
        for item in detection_data:
            class_id = item["class_id"]
            class_groups[class_id].append(item)
        
        return class_groups

    def _generate_combinations(self, processed_data, param_count, fixed_class_id=0):
        """
        특정 class_id를 고정하고 다른 class_id들과의 조합 생성
        예시: class_id 0(사람)을 고정하고 나머지 class_id들과의 조합 생성 class_id = 0 -> class_id = x (사람, 자전거), (사람, 자동차), (사람, 트럭) 등)
        """
        class_ids = list(processed_data.keys())
        combinations = []
        
        if fixed_class_id not in class_ids:
            return []
        
        other_class_ids = [cid for cid in class_ids if cid != fixed_class_id]
        
        if param_count == 1:
            for item in processed_data[fixed_class_id]:
                combo = [tuple(item["bbox"])]
                combinations.append(combo)
        elif param_count == 2:
            for other_class_id in other_class_ids:
                for item1 in processed_data[fixed_class_id]:
                    for item2 in processed_data[other_class_id]:
                        combo = [
                            tuple(item1["bbox"]),
                            tuple(item2["bbox"])
                        ]
                        combinations.append(combo)
        elif param_count == 3:
            for i in range(len(other_class_ids)):
                for j in range(i + 1, len(other_class_ids)):
                    class2, class3 = other_class_ids[i], other_class_ids[j]
                    
                    for item1 in processed_data[fixed_class_id]:
                        for item2 in processed_data[class2]:
                            for item3 in processed_data[class3]:
                                combo = [
                                    tuple(item1["bbox"]),
                                    tuple(item2["bbox"]),
                                    tuple(item3["bbox"])
                                ]
                                combinations.append(combo)
        else:
            print(f"지원하지 않는 파라미터 개수: {param_count}. 현재는 1, 2, 3개만 지원합니다.")
            return []
        return combinations
     
    def _create_file_path(self, cctv_name: str, status: str):
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        target_path = paths.VIDEO_OUTPUT_DIR / current_date
        target_path.mkdir(parents=True, exist_ok=True)
        file_path = target_path / f"{current_time}_{cctv_name}_{status}.mp4"
        return file_path