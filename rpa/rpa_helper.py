
from PySide6.QtWidgets import *  # QFileDialog 추가

###########################
### Helper Functions
###########################

# 주어진 리스트를 월요일부터 일요일 순서로 정렬하는 함수
#  ["thursday","tuesday","monday"] 같은 리스트를 월요일부터 일요일 순서로 정렬한다.
def sort_weekdays(unsorted_days):
    # 기준 요일 순서
    weekday_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # 정렬 기준: weekday_order의 인덱스를 기준으로 정렬
    return sorted(unsorted_days, key=lambda day: weekday_order.index(day.lower()))


#  영문 요일을 한글로 변환하는 함수
#  예: "monday,tuesday" -> "월,화"
def convert_weekdays_to_korean(english_days):
    # 영문 요일 -> 한글 요일 맵
    day_map = {
        "monday": "월",
        "tuesday": "화",
        "wednesday": "수",
        "thursday": "목",
        "friday": "금",
        "saturday": "토",
        "sunday": "일"
    }

    # 소문자로 변환 후, 콤마 기준으로 분리
    days = english_days.lower().split(',')

    # 변환 수행
    korean_days = [day_map.get(day.strip(), "") for day in days if day.strip() in day_map]

    return ','.join(korean_days)

#  영문 심각도를 한글로 변환하는 함수
#  예: "danger_high,danger_mid" -> "심각,위험"
def convert_severities_to_korean(english_severities):
    # 영문 요일 -> 한글 요일 맵
    severity_map = SEVERITY_MAP

    # 소문자로 변환 후, 콤마 기준으로 분리
    severities = english_severities.lower().split(',')

    # 변환 수행
    korean_days = [severity_map.get(severity.strip(), "") for severity in severities if severity.strip() in severity_map]

    return ','.join(korean_days)


def populate_grid(layout: QGridLayout, widgets: list, columns: int = 4):
    clear_grid_layout(layout)  # 기존 위젯 삭제 (앞서 만든 함수 사용)

    for i, widget in enumerate(widgets):
        row = i // columns
        col = i % columns
        layout.addWidget(widget, row, col)

def clear_grid_layout(layout: QGridLayout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)


# severity 코드 → 라벨 매핑
SEVERITY_MAP = {
        "danger_highhigh": "매우심각",
        "danger_high": "심각",
        "danger_mid": "위험",
        "danger_low": "경미",   
        "danger_lowlow": "매우경미",
        "good_highhigh": "매우우수",
        "good_high": "우수",
        "good_mid": "정상",
}

# 역매핑
SEVERITY_REVERSE_MAP = {v: k for k, v in SEVERITY_MAP.items()}

# 코드 → 라벨
def severity_to_label(code: str) -> str:
    return SEVERITY_MAP.get(code, code)

# 라벨 → 코드
def label_to_severity(label: str) -> str:
    return SEVERITY_REVERSE_MAP.get(label, label)

# 코드 리스트 → 라벨 리스트
def severity_list_to_labels(codes: list) -> list:
    return [SEVERITY_MAP.get(code, code) for code in codes]

# 라벨 리스트 → 코드 리스트
def label_list_to_severities(labels: list) -> list:
    return [SEVERITY_REVERSE_MAP.get(label, label) for label in labels]