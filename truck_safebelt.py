import cv2
import collections
from ultralytics import YOLO

MODEL_PATH = "/home/skysys/rist_model_test/SB3/best.pt"
VIDEO_PATH = "/home/skysys/rist_model_test/SB3/SB_3.mp4"
OUTPUT_PATH = "SB_3_output2.mp4"

model = YOLO(MODEL_PATH)

CLASS_NAMES = {
    0: "person",
    1: "truck",
    2: "SB_O"
}

history_sb_o = collections.deque(maxlen=10)

cap = cv2.VideoCapture(VIDEO_PATH)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    persons = []
    trucks = []
    sb_o_list = []

    # 검출 결과 정리
    for box in results.boxes:
        cls = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if cls == 0:
            persons.append((cx, cy))
        elif cls == 1:
            trucks.append((x1, y1, x2, y2))
        elif cls == 2:
            sb_o_list.append((x1, y1, x2, y2))

        # 시각화
        if cls in CLASS_NAMES:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.putText(
                frame, CLASS_NAMES[cls], (x1, y1 - 3),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )

    # 트럭 상단 ~ 1/3 ROI 안에 사람 중심점 있는지 확인
    person_in_roi = False

    for tx1, ty1, tx2, ty2 in trucks:
        h_truck = ty2 - ty1

        roi_left = tx1
        roi_right = tx2
        roi_top = ty1
        roi_bottom = ty1 + int(h_truck / 3)

        cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (255, 255, 0), 2)

        for px, py in persons:
            if roi_left <= px <= roi_right and roi_top <= py <= roi_bottom:
                person_in_roi = True
                break

        if person_in_roi:
            break

    # 최종 판단
    if not person_in_roi:
        final_signal = "GRAY"
    else:
        # 현재 프레임에서 SB_O가 하나라도 검출되면 1, 없으면 0
        history_sb_o.append(1 if len(sb_o_list) > 0 else 0)

        # 최근 10개 중 5개 이상이면 안전
        count_sb_o = sum(history_sb_o)
        final_signal = "GREEN" if count_sb_o >= 5 else "RED"

    print(final_signal)

    if out is None:
        h, w, _ = frame.shape
        out = cv2.VideoWriter(OUTPUT_PATH, fourcc, 30, (w, h))

    out.write(frame)
    cv2.imshow("Result", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()