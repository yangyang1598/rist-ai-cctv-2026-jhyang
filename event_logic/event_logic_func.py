import time
import numpy as np
import threading
from collections import deque
from rich.console import Console
console = Console()

class EventLogic:
    def __init__(self, event_data):
        self.event_data = event_data

    def is_bbox_close(self, bbox_1: tuple[int, int, int, int], bbox_2: tuple[int, int, int, int], iou_threshold: float = 0.1) -> bool:
        """
        두 bbox의 근접성을 판단합니다. 다음 조건 중 하나라도 만족하면 True를 반환합니다.
        1. 한 bbox가 다른 bbox를 완전히 포함하는 경우
        2. IoU >= iou_threshold인 경우

        Args:
            bbox_1: (x1, y1, x2, y2) 형식의 첫 번째 바운딩 박스
            bbox_2: (x1, y1, x2, y2) 형식의 두 번째 바운딩 박스
            iou_threshold: IoU 근접성 판단 임계값

        Returns:
            bool: 두 bbox가 가깝다고 판단되면 True, 아니면 False
        """

        def _compute_iou(box_a, box_b):
            x_a = max(box_a[0], box_b[0])
            y_a = max(box_a[1], box_b[1])
            x_b = min(box_a[2], box_b[2])
            y_b = min(box_a[3], box_b[3])

            intersection_area = max(0, x_b - x_a) * max(0, y_b - y_a)
            box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
            box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
            union_area = float(box_a_area + box_b_area - intersection_area)
            result = intersection_area / union_area if union_area != 0 else 0.0
            return result

        def _is_fully_contained(box_small, box_large):
            return (box_small[0] >= box_large[0] and
                    box_small[1] >= box_large[1] and
                    box_small[2] <= box_large[2] and
                    box_small[3] <= box_large[3])

        # 조건 1: 완전 포함 관계인지 확인
        if _is_fully_contained(bbox_1, bbox_2) or _is_fully_contained(bbox_2, bbox_1):
            return True
        
        # 조건 2: IoU 임계값을 넘는지 확인
        iou = _compute_iou(bbox_1, bbox_2)
        if iou >= iou_threshold:
            return True

        return False

    def is_bbox_large(self, bbox_1: tuple, image_width: int, image_height: int, threshold: int = 0.1)->bool:
        """
        바운딩 박스가 전체 화면의 threshold 비율 이상을 차지하는지 확인
        bbox: (x1, y1, x2, y2) 형식
        image_width: 이미지의 너비
        image_height: 이미지의 높이
        threshold: 화면에서 차지하는 비율 (기본값: 0.1)
        """
        bbox_width = bbox_1[2] - bbox_1[0]
        bbox_height = bbox_1[3] - bbox_1[1]
        bbox_area = bbox_width * bbox_height

        image_area = image_width * image_height

        return (bbox_area / image_area) >= threshold
    
    def detect_collision(self, detection_data: list[dict], person_class_id: int = 0,
                        target_class_id: int = 2, extend_pixel: int = 100,
                        max_window_frames_len: int = 10, min_collision_frames: int = 5):
        """
        TODO: 지게차 및 중량물 접근 감지 로직 (2025-08-18 작성중)

        접근 감지 로직
        - 화면에 사람과 지게차/중량물이 같이 검출되어, 지게차/중량물 검출 박스에 사람 box가 겹쳐지는 순간 알람 발생

        지게차/중량물과 사람 겹쳐지면 알람 -> 겹쳐지는 시간변수(시간 or frame) 에 따라 알람 발생여부 체크
        >> 모델이 깜박 거리면서 불안정할 경우 대응

        TODO: 2025-08-21 수정사항
        1. 화면에 사람과 지게차 검출
        2. 지게차 주변 +n 픽셀(변수1) ROI 설정
        3. ROI 영역 안에 사람의 중심점 진입
        4. 2초(10프레임, 변수2) 안에 사람의 중심점이 ROI 영역 내부에 1초(5프레임, 변수3) 동안 있으면 알람 발생
            >> 예시) 0프레임 안에 사람 중심점이 지게차 ROI 영역 내부에 0프레임 동안 있으면 알람 → 즉시 알람
            >> 10프레임 안에 사람 중심점이 지게차 ROI 영역 내부에 5프레임 이상 있으면 알람 → 판단 후 알람

        * 각 변수들은 외부에서 설정 가능해야 함
        """

        def is_center_in_bbox(person_bbox, target_bbox):
            center_x = (person_bbox[0] + person_bbox[2]) / 2
            center_y = (person_bbox[1] + person_bbox[3]) / 2
            
            return (target_bbox[0] <= center_x <= target_bbox[2] and
                    target_bbox[1] <= center_y <= target_bbox[3])

        # 함수 속성으로 카운터 초기화 (최초 호출 시에만)
        if not hasattr(self, "collision_frame_count"):
            self.collision_frame_count = 0
            self.window_frames: deque = deque(maxlen=max_window_frames_len)

        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        targets = [d for d in detection_data if d["class_id"] == target_class_id]
        collision_detected = False

        # 현재 프레임에서 충돌 여부 한 번만 판단
        for target in targets:
            target_bbox = target["bbox"]
            extend_target_bbox = np.array(target_bbox) 
            extend_target_bbox[:2] -= extend_pixel
            extend_target_bbox[2:] += extend_pixel

            for person in persons:
                if is_center_in_bbox(person["bbox"], extend_target_bbox):
                    collision_detected = True
                    break
            if collision_detected:
                break

        # 즉시 알람 조건 (min_collision_frames = 0인 경우)
        if min_collision_frames == 0:
            return collision_detected # 현재 프레임의 충돌 여부를 바로 반환
    
        # 현재 프레임 결과를 윈도우에 추가 (매 프레임마다 1개만)
        self.window_frames.append(collision_detected)

        # 윈도우 내 충돌 프레임 수 확인
        collision_count = sum(self.window_frames)
        # console.log(f"[bold yellow]슬라이딩 윈도우 내 충돌 횟수: {collision_count}/{len(self.window_frames)} (최소 {min_collision_frames} 회)[/bold yellow]")
        if collision_count >= min_collision_frames:
            # console.log(f"[bold red]🚨 충돌 발생: {collision_count}/{len(self.window_frames)} 프레임[/bold red]")
            return True
        return False
    
    def bulti(self, detection_data: list[dict], fire_spark_class_id:int = 1, smoke_class_id:int = 0, extend_pixel:int = 100, roi_duration_time:int = 10) -> bool:
        """
        불티 감지 시 독립적인 타이머를 실행하여 상태를 추적하고,
        ROI 내 연기 감지 시 알람을 발생시키는 함수.
        """
        # --- 내부 변수 및 함수 초기화 (최초 1회만 실행) ---
        if not hasattr(self, '_internal_state'):
            # bulti 함수에 필요한 모든 상태를 저장하는 객체
            self._internal_state = {
                'roi_box': None,
                'active_timer': None, # 현재 활성화된 threading.Timer 객체
                'lock': threading.Lock(), # 상태 변수 동시 접근 방지용
                "last_log_time": 0.0, # 로그 출력 시간 제어용
            }

            def _timer_tick(remaining_seconds: int):
                """
                1초마다 호출되어 카운트다운을 수행하는 내부 함수.
                """
                state = self._internal_state
                with state['lock']:
                    # 타이머가 외부(새로운 불티 감지 등)에서 이미 취소된 경우, 아무 작업도 하지 않음
                    if not state['active_timer']:
                        return

                    # 1. 카운트다운 종료 조건
                    if remaining_seconds <= 0:
                        console.log(f"[bold orange1]⏰ 타이머 만료. ROI를 리셋합니다.[/bold orange1]")
                        state['roi_box'] = None
                        state['active_timer'] = None
                        return

                    # 2. 다음 틱 예약 및 로그 출력
                    console.log(f"[bold orange1]⏰ ROI 활성 중... 남은시간: {remaining_seconds}초[/bold orange1]")
                    
                    # 1초 후에 자기 자신을 다시 호출하는 새로운 타이머 생성 및 시작
                    next_timer = threading.Timer(1.0, self._timer_tick, args=[remaining_seconds - 1])
                    state['active_timer'] = next_timer
                    next_timer.start()

            # 내부 함수를 클래스 메서드처럼 self에 바인딩하여 상태를 공유
            self._timer_tick = _timer_tick
        
        # --- 기본 설정 및 변수 ---
        state = self._internal_state
        roi_padding_pixels = extend_pixel
        
        with state['lock']:
            fire_sparks = [d for d in detection_data if d["class_id"] == fire_spark_class_id]
            smokes = [d for d in detection_data if d["class_id"] == smoke_class_id]

            # --- 1. 불티 감지 처리 ---
            if fire_sparks:
                # 1-1. 기존에 실행 중인 타이머가 있다면 즉시 취소
                if state['active_timer']:
                    state['active_timer'].cancel()
                    state['active_timer'] = None # 타이머 객체 참조 제거

                # 1-2. 새로운 ROI 계산 및 설정
                x1, y1, x2, y2 = fire_sparks[0]["bbox"]
                state['roi_box'] = (
                    max(0, x1 - roi_padding_pixels),
                    max(0, y1 - roi_padding_pixels),
                    x2 + roi_padding_pixels,
                    y2 + roi_padding_pixels
                )

                current_time = time.time()
                if current_time - state.get('last_log_time', 0.0) >= 1.0:
                    state['last_log_time'] = current_time
                #     console.log(f"[bold cyan]🔥 불티 감지! ROI: {state['roi_box']}[/bold cyan]")

                # 1-3. 새로운 타이머 시작
                new_timer = threading.Timer(1.0, self._timer_tick, args=[roi_duration_time - 1])
                state['active_timer'] = new_timer
                new_timer.start()
                return False

            # --- 2. 연기 감지 처리 (ROI가 활성화된 경우) ---
            if state['roi_box'] and smokes:
                roi_x1, roi_y1, roi_x2, roi_y2 = state['roi_box']
                for smoke in smokes:
                    smoke_x1, smoke_y1, smoke_x2, smoke_y2 = smoke["bbox"]
                    if not (smoke_x2 < roi_x1 or smoke_x1 > roi_x2 or smoke_y2 < roi_y1 or smoke_y1 > roi_y2):
                        console.log(f"🚨 [bold red]화재 알람! ROI 영역 내에서 연기 감지됨.[/bold red]")
                        
                        # 실행 중인 타이머 취소
                        if state['active_timer']:
                            state['active_timer'].cancel()

                        # 상태 초기화
                        state['roi_box'] = None
                        state['active_timer'] = None
                        return True

        return False

    def jiguk1(self, detection_data: list[dict]) -> dict:
        """
        지적확인 로직1
        - 화면에 지적확인 개소 검출 → 검출된 개소 내부에 사람 검출 박스 진입  →   사람 내부에 지적확인 박스 중심점 검출 여부 확인 (per person)
        Args:
            detection_data (List[dict]): 객체 검출 결과 데이터, 각 객체는 다음과 같은 형식:
                {
                    'id': int,                # 객체 ID (트래킹 ID)
                    'class_id': int,          # 객체 클래스 ID (0: 사람, 1: 지적확인 행동, 2: 지적확인 개소)
                    'confidence': float,      # 신뢰도
                    'bbox': [x1, y1, x2, y2]  # 바운딩 박스 좌표
                }

        Returns:
            dict: 지적확인 결과
                {
                    'person_ids': list[int],                  # 검출된 모든 사람 객체 ID 리스트
                    'site_entered': bool,                     # 지적확인 개소에 최소 한 명의 사람 진입 여부
                    'site_entered_person_ids': list[int],     # 개소에 진입한 사람 ID 리스트 (IoU > 0)
                    'person_jiguk_not_detected': dict[int, bool]  # 각 진입 사람 ID별 지적확인 행동 미검출 여부 (True: 미검출, False: 검출)
                }
        """
        
        # class_id별 객체 분류
        people_bboxes = {obj['track_id']: obj['bbox'] for obj in detection_data if obj['class_id'] == 0}  # 사람: id -> bbox
        jiguk_bboxes = [obj['bbox'] for obj in detection_data if obj['class_id'] == 1]  # 지적확인 행동: bboxes 리스트
        # space_bboxes = [obj['bbox'] for obj in detection_data if obj['class_id'] == 2]  # 지적확인 개소: bboxes 리스트
        space_bboxes = [obj['bbox'] for obj in detection_data if obj.get('filter') is True and obj.get('class_id') not in (0, 1)]
        
        person_ids = list(people_bboxes.keys())
        
        # 1. 지적확인 개소(들)에 사람 진입 여부 확인 (IoU > 0, 여러 개소 지원)
        site_entered_person_ids = set()
        for person_id, person_bbox in people_bboxes.items():
            for space_bbox in space_bboxes:
                if self.is_bbox_close(person_bbox, space_bbox):
                    site_entered_person_ids.add(person_id)
                    break  # 해당 사람에 대해 하나의 개소라도 겹치면 충분
        
        site_entered = bool(site_entered_person_ids)
        
        # 2. 진입한 각 사람별 지적확인 행동 검출 여부 (지적확인 행동 중심점이 사람 bbox 내부에 있는지)
        person_jiguk_not_detected = {}
        if site_entered:
            for person_id in site_entered_person_ids:
                person_bbox = people_bboxes[person_id]
                jiguk_detected = False
                for jiguk_bbox in jiguk_bboxes:
                    center_x = (jiguk_bbox[0] + jiguk_bbox[2]) / 2
                    center_y = (jiguk_bbox[1] + jiguk_bbox[3]) / 2
                    if (person_bbox[0] <= center_x <= person_bbox[2] and 
                        person_bbox[1] <= center_y <= person_bbox[3]):
                        jiguk_detected = True
                        break
                person_jiguk_not_detected[person_id] = not jiguk_detected  # True: 미검출, False: 검출
        
        result = {
            'person_ids': person_ids,
            'site_entered': site_entered,
            'site_entered_person_ids': list(site_entered_person_ids),
            'person_jiguk_not_detected': person_jiguk_not_detected
        }
        return result
    
    def jiguk2(self, detection_data: list[dict]):
        """
        지적확인 로직2
        1) 화면에서 지적확인 개소 검출
        2) 검출된 개소 내부에 사람 검출 박스 진입 
        3) 영상 저장 (트리거) 시작
        4) 지적확인 장소에 n초 이상 있는지 확인 → n초 설정 시간이상 머무를시 →영상 저장 안함 → 같은 ID는 재검출 안함 → n초 설정 이내 지적확인 장소 밖으로 나갈시 로직 5) 실행
        5) 로직(방향성 판단) 실행
            - 로직(방향성 판단)이 설정한 조건과 다를시 영상 저장 안함  → UI 화면에 알람 발생X
            - 로직(방향성 판단)이 설정한 조건과 동일시 → 지적확인 프레임 확인 → UI 화면에 알람 발생X  → 영상 저장을 “지적확인 실시” 파일명 저장
            - 로직(방향성 판단)이 설정한 조건과 동일시 → 지적확인 프레임 미확인 → UI 화면에 2초간 알람 발생O → 영상 저장을 “지적확인 미실시” 파일명 저장
            ※ 영상 저장 종료 시점(트리거)은 지정확인장소 밖으로 나갔을때

        5)의 로직(방향성 판단) 세부 내용:
        지적확인 장소에 들어오는 첫프레임 + 지적확인 장소에서 나가는 마지막 프레임 비교를 통한 방향성 판단
        사람이 지적확인 장소에 들어오는 첫프레임A (x1,y1)와 지적확인 장소를 벗어났을때의 전 프레임B (x2, y2)
        △x= x2-x1, △y = y2-y1
        왼쪽에서 오른쪽으로 이동하는 사람의 X축의 변화량 판단으로 |△x| < | △y | 일때,  X축의 이동이 아니라고 판단 -> 거짓
        왼쪽에서 오른쪽으로 이동하는 사람의 X축의 변화량 판단으로 |△x| > | △y | 일때, X축의 이동이라고  판단 -> 참
        2-a일 경우 △x의 양과 음을 판단하여 왼쪽에서 오른쪽 이동일 경우 양(+)             → True
                                                오른쪽에서 왼쪽으로 이동일 경우 음(-)  → False

        """

        # class_id별 객체 분류
        people_bboxes = {obj['track_id']: obj['bbox'] for obj in detection_data if obj['class_id'] == 0}  # 사람: id -> bbox
        jiguk_bboxes = [obj['bbox'] for obj in detection_data if obj['class_id'] == 1]  # 지적확인 행동: bboxes 리스트
        # space_bboxes = [obj['bbox'] for obj in detection_data if obj['class_id'] == 2]  # 지적확인 개소: bboxes 리스트
        space_bboxes = [obj['bbox'] for obj in detection_data if obj.get('filter') is True and obj.get('class_id') not in (0, 1)]
        
        person_ids = list(people_bboxes.keys())
        
        # 1. 지적확인 개소(들)에 사람 진입 여부 확인 (IoU > 0, 여러 개소 지원)
        site_entered_person_ids = set()
        for person_id, person_bbox in people_bboxes.items():
            for space_bbox in space_bboxes:
                if self.is_bbox_close(person_bbox, space_bbox):
                    site_entered_person_ids.add(person_id)
                    break  # 해당 사람에 대해 하나의 개소라도 겹치면 충분
        
        site_entered = bool(site_entered_person_ids)
        
        # 2. 진입한 각 사람별 지적확인 행동 검출 여부 (지적확인 행동 중심점이 사람 bbox 내부에 있는지)
        person_jiguk_not_detected = {}
        if site_entered:
            for person_id in site_entered_person_ids:
                person_bbox = people_bboxes[person_id]
                jiguk_detected = False
                for jiguk_bbox in jiguk_bboxes:
                    center_x = (jiguk_bbox[0] + jiguk_bbox[2]) / 2
                    center_y = (jiguk_bbox[1] + jiguk_bbox[3]) / 2
                    if (person_bbox[0] <= center_x <= person_bbox[2] and 
                        person_bbox[1] <= center_y <= person_bbox[3]):
                        jiguk_detected = True
                        break
                person_jiguk_not_detected[person_id] = not jiguk_detected  # True: 미검출, False: 검출
        
        result = {
            'person_ids': person_ids,
            'site_entered': site_entered,
            'site_entered_person_ids': list(site_entered_person_ids),
            'person_jiguk_not_detected': person_jiguk_not_detected
        }
        return result

    def safebelt1(self, detection_data: list[dict], person_class_id: int = 0, safebelt_class_id: int = 4,
                hook_class_id: int = 5, hook_connection_class_id: int = 6, max_deque_size: int = 10) -> bool:
        """
        1. CCTV 화면에서 사람이 검출되고, 사람 box 내부에 안전대 검출이 n초동안 1프레임이라도 안되면 알람 발생 → 이미지 캡처 (지적확인과 동일한 Tracking을 사용하여 동일한 사람일 경우 재알람 발생 X) 
        2. CCTV 화면에서 n초동안 안전대가 1프레임이라도 검출되고, 안전고리 1개만 검출되거나 2개가 겹쳐지지 않은 상태로 검출되면 알람 발생
        (사람 Tracking을 사용하여 동일한 사람의 알람일 경우 재알람 발생 X) 
        3. n초 동안 connect_hook가 검출 안되어도, hook 2개가 검출되고 2개의 hook box가 겹쳐지면 알람 발생X
        (사람 Tracking을 사용하여 동일한 사람의 알람일 경우 재알람 발생 X) 
        4. n 초 동안 안전고리가 1개만 검출되고, 안전대가 검출 안되어도 hook_connection 검출이 뜨면 알람 발생 X
        """
        if not hasattr(self, "person_safebelt_history"):
            self.person_safebelt_history: dict[int, deque] = {}
            self.alerted_persons: set[int] = set()

        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        safebelts = [d for d in detection_data if d["class_id"] == safebelt_class_id]
        hooks = [d for d in detection_data if d["class_id"] == hook_class_id]
        hook_connections = [d for d in detection_data if d["class_id"] == hook_connection_class_id]

        # console.log(persons)
        # console.log(safebelts)
        # console.log(hooks)
        # console.log(hook_connections)

        # 사람 검출 안되면 pass
        if not persons:
            return False

        # 각 사람별 안전대 검출 체크
        for person in persons:
            px1, py1, px2, py2 = person.get("bbox", (0,0,0,0))
            person_id: int = int(person.get("track_id", -1))

            if person_id not in self.person_safebelt_history:
                self.person_safebelt_history[person_id] = deque(maxlen=max_deque_size)

            # 현재 프레임에서 안전대 검출 여부
            safebelt_detected = False
            for safebelt in safebelts:
                sx1, sy1, sx2, sy2 = safebelt.get("bbox", (0,0,0,0))
                center_x = (sx1 + sx2) / 2
                center_y = (sy1 + sy2) / 2
                if px1 <= center_x <= px2 and py1 <= center_y <= py2:
                    safebelt_detected = True
                    break
            self.person_safebelt_history[person_id].append(safebelt_detected)
            
        # 체크 로직 1 - 각 사람 별 box 내부에 안전대가 모두 검출되었는지 체크
        for person_id, detection_history in self.person_safebelt_history.items():
            if len(detection_history) < max_deque_size:
                continue  # 아직 충분한 데이터가 쌓이지 않음
            # console.log(f"Person ID: {person_id}, Safebelt Detection History: {list(detection_history)}")

            if person_id in self.alerted_persons:
                continue  # 이미 알람이 발생한 사람은 무시

            if not all(detection_history):
                console.log(f"[bold red]🚨 안전대 미착용 알람! 사람 ID: {person_id}[/bold red]")
                self.person_safebelt_history[person_id].clear()  # 알람 후 기록 초기화
                self.alerted_persons.add(person_id) # 안전대 미착용한 인원 id 저장
                return True  # 안전대 미착용 알람 발생
        
            # 체크로직 2 - 안전고리 검출 체크
            # 안전고리 1개 검출 상황
            # console.log(f"hooks: {len(hooks)}, hook_connections: {len(hook_connections)}")
            if len(hooks) == 1 and not hook_connections:
                console.log(f"[bold red]🚨 안전고리 1개 - 미착용 알람! 사람 ID: {person_id}[/bold red]")
                self.alerted_persons.add(person_id)
                return True
            
            # 안전고리 2개 검출 상황
            elif len(hooks) >= 2:
                if hook_connections:
                    pass
                # bbox 겹침 체크 필요
                elif not self.is_bbox_close(hooks[0]["bbox"], hooks[1]["bbox"]):
                    console.log(f"[bold red]🚨 안전고리 2개 - 미착용 알람! 사람 ID: {person_id}[/bold red]")
                    self.alerted_persons.add(person_id)
                    return True
            
        # console.log(f"[bold green]✅ 위험 상황 없음! 사람 ID: {person_id}[/bold green]")
        return False

    def safebelt2(self, detection_data: list[dict],  person_class_id: int = 0, safebelt_class_id: int = 4,
                hook_class_id: int = 5, open_door_class_id: int = 9, max_deque_size: int = 10, roi_extend_pixel: int = 100) -> bool:
        """
        1. CCTV 화면에서 Open_door이 검출되면 open_door 주변 영역 +100픽셀에 ROI 영역 설정
        2. Open_door이 검출이 안되면 알람 발생X(로직 구동 필요없음)
        3. 사람 box가 open_door box와 겹쳐있으면 안전대 안전고리가 검출되었는지 확인 시작
        4. 겹쳐지는 이후부터 n초 동안 안전대가 1프레임이라도 검출되면 알람 발생X
        5. 겹쳐지는 순간부터 n초 동안 (안전대가 미검출되었더라도) Hook가 1프레임이라도 검출되면 알람 발생 X
        6. 사람과 open_door이 겹쳐지지 않으면 n초는 초기화

        'names': {0: 'person', 1: 'lift', 2: 'forklift', 3: 'gagubu', 4: 'safebelt', 5: 'hook', 6: 'connect_hook', 7: 'flash_suit', 8: 'waldam', 9: 'open_door', 10: 'flash_fire', 11: 'falldown'}
        """

        if not hasattr(self, "person_safebelt_history"):
            self.person_safebelt_history: dict[int, deque] = {}
            self.person_hook_history: dict[int, deque] = {}
            self.alerted_persons: set[int] = set()

        open_doors = [d for d in detection_data if d["class_id"] == open_door_class_id]
        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        safebelts = [d for d in detection_data if d["class_id"] == safebelt_class_id]
        hooks = [d for d in detection_data if d["class_id"] == hook_class_id]

        # open_door 검출 안되면 로직 작동X
        if not open_doors:
            return False
        # console.log(f"[bold cyan]🚪 Open_door 검출됨. 안전대 및 안전고리 검출 로직 작동 시작...[/bold cyan]")
        
        overlapped_persons = set()

        # person과 open_door이 겹쳐지는지 확인
        for person in persons:
            px1, py1, px2, py2 = person.get("bbox", (0,0,0,0))
            person_id: int = int(person.get("track_id", -1))
            is_overlapped = False

            if person_id not in self.person_safebelt_history:
                self.person_safebelt_history[person_id] = deque(maxlen=max_deque_size)
                self.person_hook_history[person_id] = deque(maxlen=max_deque_size)

            for open_door in open_doors:
                open_door_bbox = open_door.get("bbox", (0,0,0,0))
                extend_open_door_bbox = np.array(open_door_bbox) 
                extend_open_door_bbox[:2] -= roi_extend_pixel
                extend_open_door_bbox[2:] += roi_extend_pixel

                # person과 open_door이 겹쳐짐
                if self.is_bbox_close(person["bbox"], extend_open_door_bbox):
                    is_overlapped = True
                    # console.log(f"[bold yellow] 사람 ID {person_id}이(가) Open_door과 겹쳐짐. 안전대 및 안전고리 검출 체크 시작...[/bold yellow]")
                    overlapped_persons.add(person_id)

                    # 현재 프레임에서 안전대 검출 여부
                    safebelt_detected = False
                    for safebelt in safebelts:
                        sx1, sy1, sx2, sy2 = safebelt.get("bbox", (0,0,0,0))
                        center_x = (sx1 + sx2) / 2
                        center_y = (sy1 + sy2) / 2
                        if px1 <= center_x <= px2 and py1 <= center_y <= py2:
                            safebelt_detected = True
                            break
                    self.person_safebelt_history[person_id].append(safebelt_detected)

                    # 현재 프레임에서 안전고리 검출 여부
                    hook_detected = False
                    if hooks:
                        hook_detected = True
                    # for hook in hooks:
                    #     hx1, hy1, hx2, hy2 = hook.get("bbox", (0,0,0,0))
                    #     center_x = (hx1 + hx2) / 2
                    #     center_y = (hy1 + hy2) / 2
                    #     # person 영역 내에 hook의 중심점이 있는지 확인
                    #     if px1 <= center_x <= px2 and py1 <= center_y <= py2:
                    #         hook_detected = True
                    #         break
                    self.person_hook_history[person_id].append(hook_detected)

                    # console.log(f"[bold] 사람 ID: {person_id}, Safebelt Detection History: {list(self.person_safebelt_history[person_id])}[/bold]")
                    # console.log(f"[bold] 사람 ID: {person_id}, Hook Detection History: {list(self.person_hook_history[person_id])}[/bold]")

            # person과 open_door이 겹쳐지지 않으면 n초는 초기화
            if not is_overlapped and person_id in self.person_safebelt_history:
                self.person_safebelt_history[person_id].clear()
                self.person_hook_history[person_id].clear()

        # person과 open_door이 겹쳐진 상태에서 안전대 및 안전고리 검출 체크
        for person_id in overlapped_persons:
            if len(self.person_safebelt_history[person_id]) >= max_deque_size:
                safebelt_detected = any(self.person_safebelt_history[person_id])
                hook_detected = any(self.person_hook_history[person_id])
                
                if not safebelt_detected and not hook_detected:
                    return True  # 알람 발생
        
        # console.log(f"[bold green]✅ 위험 상황 없음![/bold green]")
        return False

    def safebelt3(self, detection_data: list[dict], person_class_id: int = 0,
                truck_class_id: int = 1, sb_o_class_id: int = 2,
                max_deque_size: int = 10, sb_o_threshold: int = 5) -> bool:
        """
        트럭 안전벨트 감지 로직
        1. truck 검출 시 truck bbox 상단 1/3 영역을 ROI로 설정
        2. person 중심점이 ROI 내에 있으면 안전벨트 체크 시작
        3. ROI 내 사람이 있는 상태에서 최근 max_deque_size 프레임 중 SB_O 검출이 sb_o_threshold 미만이면 알람 발생 (미착용)
        4. person이 ROI에 없으면 판단하지 않음 (GRAY)
        """
        if not hasattr(self, "sb_o_history"):
            self.sb_o_history: deque = deque(maxlen=max_deque_size)

        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        trucks = [d for d in detection_data if d["class_id"] == truck_class_id]
        sb_o_list = [d for d in detection_data if d["class_id"] == sb_o_class_id]

        if not trucks:
            return False

        # 트럭 상단 1/3 ROI 내에 사람 중심점이 있는지 확인
        person_in_roi = False
        for truck in trucks:
            tx1, ty1, tx2, ty2 = truck.get("bbox", (0, 0, 0, 0))
            h_truck = ty2 - ty1
            roi_bottom = ty1 + int(h_truck / 3)

            for person in persons:
                px1, py1, px2, py2 = person.get("bbox", (0, 0, 0, 0))
                cx = (px1 + px2) // 2
                cy = (py1 + py2) // 2
                if tx1 <= cx <= tx2 and ty1 <= cy <= roi_bottom:
                    person_in_roi = True
                    break
            if person_in_roi:
                break

        if not person_in_roi:
            return False

        # SB_O 검출 이력 기록
        self.sb_o_history.append(1 if len(sb_o_list) > 0 else 0)

        # 이력이 충분히 쌓이면 판단
        if len(self.sb_o_history) >= max_deque_size:
            count_sb_o = sum(self.sb_o_history)
            if count_sb_o < sb_o_threshold:
                return True  # 안전벨트 미착용 → 알람

        return False

    def safebelt4(self, detection_data: list[dict], person_class_id: int = 0, truck_class_id: int = 1,
                    max_deque_size: int = 10, person_threshold: int = 5) -> bool:
        """
        트럭 상부 사람 체류 감지 로직
        1. truck 검출 시 truck bbox 상단 1/2 영역을 ROI로 설정
        2. 매 프레임마다 person 중심점이 ROI 내에 있는지 여부를 기록
        3. 최근 max_deque_size 프레임 중 person_threshold 이상 ROI 내 사람이 검출되면 알람 발생
        4. truck이 검출되지 않으면 판단하지 않음
        """
        if not hasattr(self, "person_in_roi_history"):
            self.person_in_roi_history: deque = deque(maxlen=max_deque_size)

        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        trucks = [d for d in detection_data if d["class_id"] == truck_class_id]

        if not trucks:
            return False

        # 트럭 상단 1/2 ROI 내에 사람 중심점이 있는지 확인
        person_in_roi = False
        for truck in trucks:
            tx1, ty1, tx2, ty2 = truck.get("bbox", (0, 0, 0, 0))
            h_truck = ty2 - ty1
            roi_bottom = ty1 + int(h_truck / 2)

            for person in persons:
                px1, py1, px2, py2 = person.get("bbox", (0, 0, 0, 0))
                cx = (px1 + px2) // 2
                cy = (py1 + py2) // 2
                if tx1 <= cx <= tx2 and ty1 <= cy <= roi_bottom:
                    person_in_roi = True
                    break
            if person_in_roi:
                break

        # 매 프레임마다 ROI 진입 여부를 기록
        self.person_in_roi_history.append(1 if person_in_roi else 0)

        # 이력이 충분히 쌓이면 판단
        if len(self.person_in_roi_history) >= max_deque_size:
            count = sum(self.person_in_roi_history)
            if count >= person_threshold:  # ← 이상이면 알람
                return True

        return False

    def flash_suit(self, detection_data: list[dict], person_class_id: int = 0,
                flash_fire_class_id: int = 2, flash_suit_class_id: int = 7,
                roi_extend_pixel: int = 500, min_deque_size: int = 10) -> bool:
        """
        1. CCTV 화면에서 flash_fire이 없으면 로직 작동X
        2. flash_fire이 검출되면 주변 영역 +500픽셀에 ROI 영역 설정
        3. ROI 영역에 사람이 진입하면 검출된 사람 box 내부에 방염복(flash_suit) 박스의 중심점이 있으면 알람 발생X
        4. n초 동안 방염복을 확인하고 미검출시 알람 발생
        5. Tracking을 써서 동일한 ID인데 방염복 검출이 깜박 깜박여도 알람 발생X
        6. flash_fire이 사라지면 초기화 n초는 초기화
        """
        if not hasattr(self, "person_flash_suit_history"):
            self.person_flash_suit_history: dict[int, deque] = {}
            self.alerted_flash_suit_persons: set[int] = set()

        # console.log(detection_data)
        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        fires = [d for d in detection_data if d["class_id"] == flash_fire_class_id]
        suits = [d for d in detection_data if d["class_id"] == flash_suit_class_id]

        if not fires:
            self.person_flash_suit_history.clear()
            return False
        
        roi_entered_persons = set()

        for fire in fires:
            # flash_fire 주변 +500 픽셀에 ROI 영역 설정
            fire_bbox = fire["bbox"]
            extend_fire_bbox = np.array(fire_bbox) 
            extend_fire_bbox[:2] -= roi_extend_pixel
            extend_fire_bbox[2:] += roi_extend_pixel

            # ROI 영역에 사람이 진입했는지 확인
            for person in persons:
                person_id = int(person.get("track_id", -1))
                px1, py1, px2, py2 = person["bbox"]

                if self.is_bbox_close(person["bbox"], extend_fire_bbox):
                    # 진입한 사람 내부에 방염복 중심점이 있는지 확인
                    roi_entered_persons.add(person_id)

                    if person_id not in self.person_flash_suit_history:
                        self.person_flash_suit_history[person_id] = deque(maxlen=min_deque_size)

                    suit_found = False
                    for suit in suits:
                        sx1, sy1, sx2, sy2 = suit["bbox"]
                        center_x = (sx1 + sx2) / 2
                        center_y = (sy1 + sy2) / 2
                        if (px1 <= center_x <= px2 and py1 <= center_y <= py2):
                            suit_found = True
                            # console.log(f"[bold green]✅ 방염복 착용 확인! 사람 ID: {person['track_id']}[/bold green]")
                            break

                    self.person_flash_suit_history[person_id].append(suit_found)

        # ROI 영역을 벗어난 사람의 히스토리 초기화
        for person_id in list(self.person_flash_suit_history.keys()):
            if person_id not in roi_entered_persons:
                self.person_flash_suit_history[person_id].clear()
        
        # n초(min_deque_size 프레임) 동안 방염복 검출 여부 확인
        for person_id, detection_history in self.person_flash_suit_history.items():
            if len(detection_history) < min_deque_size:
                continue
            
            # 이미 알람이 발생한 사람은 무시
            if person_id in self.alerted_flash_suit_persons:
                continue
            
            # n초 동안 방염복이 한 번이라도 검출되었는지 확인
            if any(detection_history):
                # console.log(f"[bold green]✅ 방염복 착용 확인! 사람 ID: {person_id}[/bold green]")
                continue
            else:
                # n초 동안 방염복이 한 번도 검출되지 않음
                # console.log(f"[bold red]🚨 방염복 미착용 알람! 사람 ID: {person_id}[/bold red]")
                self.alerted_flash_suit_persons.add(person_id)
                self.person_flash_suit_history[person_id].clear()
                return True

        return False

    def waldam(self, detection_data: list[dict], person_class_id: int = 0, space_class_id: int = 1, waldam_class_id: int = 2) -> bool:
        """
        월담 검출 개소에 진입한 사람 객체의 bbox 내부에 월담 객체의 중심점이 존재하면 알람
        사람이 여러명 있을 경우 사람 내부에 월담 객체의 중심점이 1개라도 있으면 알람
        """

        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        spaces = [d for d in detection_data if d["class_id"] == space_class_id]
        waldams = [d for d in detection_data if d["class_id"] == waldam_class_id]

        if not waldams:
            return False
        
        for space in spaces:
            for person in persons:
                if not self.is_bbox_close(space["bbox"], person["bbox"]):
                    continue
                else:
                    px1, py1, px2, py2 = person["bbox"]
                    for target in waldams:
                        tx1, ty1, tx2, ty2 = target["bbox"]
                        center_x = (tx1 + tx2) / 2
                        center_y = (ty1 + ty2) / 2
                        if (px1 <= center_x <= px2) and (py1 <= center_y <= py2):
                            # console.log(f"[bold red]🚨 월담 알람! 사람 ID: {person['track_id']}[/bold red]")
                            return True
        return False
    
    def falldown(self, detection_data: list[dict], person_class_id: int = 0, target_class_id: int = 9) -> bool:
        """
        검출된 사람 객체의 bbox 내부에 x 객체의 중심점이 존재하면 알람
        사람이 여러명 있을 경우 사람 내부에 x 객체의 중심점이 1개라도 있으면 알람
        """

        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        targets = [d for d in detection_data if d["class_id"] == target_class_id]

        if not targets:
            return False
        
        for person in persons:
            px1, py1, px2, py2 = person["bbox"]
            for target in targets:
                tx1, ty1, tx2, ty2 = target["bbox"]
                center_x = (tx1 + tx2) / 2
                center_y = (ty1 + ty2) / 2
                if (px1 <= center_x <= px2) and (py1 <= center_y <= py2):
                    # console.log(f"[bold red]🚨 쓰러짐 알람! 사람 ID: {person['track_id']}[/bold red]")
                    return True

        return False

    def person_count(self, detection_data: list[dict], person_class_id: int = 0) -> int:
        """
        화면에 검출된 사람 객체 수를 반환하는 함수.
        """
        persons = [d for d in detection_data if d["class_id"] == person_class_id]
        return len(persons)
    
    def test_function(self, bbox_1: tuple, bbox_2: tuple) -> bool:
        """
        테스트용 함수로, 인자로 받은 값을 그대로 반환합니다.
        """
        print(f"다른 함수에서 불러옵니다: {bbox_1}, bbox_2: {bbox_2}")
        return True