import os
import json
import numpy as np
from ultralytics import YOLO
from rich.traceback import install
from rich.console import Console
from rich.table import Table
install()
console = Console()

class NumpyEncoder(json.JSONEncoder):
    """
    NumpyEncoder 클래스는 numpy 데이터 타입을 JSON serializable 객체로 변환하기 위해 설계되었습니다.

    주요 기능
    ----------
    - numpy.integer: 정수형 객체를 파이썬의 int 타입으로 변환합니다.
    - numpy.floating: 부동 소수점 객체를 파이썬의 float 타입으로 변환합니다.
    - numpy.ndarray: 배열 객체를 파이썬의 리스트로 변환합니다.
    - 그 외의 타입에 대해서는 상위 클래스의 default 메서드를 호출하여 처리합니다.

    메서드
    ------
    default(obj)
        JSON 인코딩이 지원되지 않는 객체를 적절한 파이썬 기본 타입으로 변환합니다.
        만약 obj가 numpy 데이터 타입이면 해당 타입에 맞게 변환을 수행하고,
        그렇지 않을 경우 상위 클래스의 default 메서드를 호출합니다.

    참고
    -----
    이 클래스는 numpy 배열 및 스칼라 값의 직렬화를 쉽게 하기 위해 사용됩니다.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)
   
# 2025.05.21 수정 (박보은) 
def model_performance_value(project: str, name: str, data: str):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! performance value start")
    PROJECT = project

    model_a = f"{PROJECT}/{name}/weights/best.pt"
    # YOLO 모델 로드
    model = YOLO(model_a, task="detect")

    # 검증 수행
    val_results = model.val(project=PROJECT, name=name, data=data, imgsz=640, verbose=False)

    result_dict = "test"
    # 메트릭 추출
    results_dict = val_results.results_dict
    precision, recall, map50, map5095 = [results_dict[key] for key in val_results.keys]

    # F1 Score 계산
    denominator = precision + recall
    f1_score = np.divide(2 * precision * recall, denominator, out=np.zeros_like(denominator), where=denominator != 0)

    # 소수점 반올림
    metrics_array = np.array([precision, recall, map50, map5095, f1_score])
    rounded_metrics = np.round(metrics_array, 4)

    # 클래스별 mAP 데이터 추출
    maps = val_results.box.maps  # 클래스별 mAP 점수
    ap_class_index = val_results.box.ap_class_index  # 검출된 클래스 인덱스
    names = val_results.names  # 클래스 이름 딕셔너리
    maps_rounded = np.round(maps, 4)  # 소수점 반올림

    # model.val()의 speed 값 사용
    speed = val_results.speed['inference']  # 검증 데이터셋의 평균 추론 시간
    print(f"main: {speed}")

    # 클래스별 메트릭 딕셔너리 생성
    class_metrics = {}
    if len(ap_class_index) > 0:
        for j, class_idx in enumerate(ap_class_index):
            class_name = names[class_idx]
            class_metrics[class_name] = [class_idx, maps_rounded[j]]

    # 결과 딕셔너리 생성 - 미리 계산된 값 사용
    result_dict = {
        "Model": model_a,
        "Metrics": {
            "precision": rounded_metrics[0],
            "recall": rounded_metrics[1],
            "map50": rounded_metrics[2],
            "map50_95": rounded_metrics[3],
            "f1_score": rounded_metrics[4],
            "speed": speed  # model.val()의 speed 값 사용
        },
    }

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! performance value end")
    return result_dict

def ab_test(model_a: str, model_b: str):
    """
    두 모델의 평가를 수행하여 메트릭을 비교합니다.

    Parameters
    ----------
    model_a : str
        첫 번째 모델의 파일 경로.
    model_b : str
        두 번째 모델의 파일 경로.
    
    Returns
    -------
    list of dict
        각 모델에 대한 평가 결과를 담은 딕셔너리들의 리스트.
        각 딕셔너리는 다음과 같은 구조를 가집니다.
            - "Model": 모델 파일 경로 (str)
            - "Metrics": 평가 메트릭을 담은 딕셔너리
                * "Precision": 정밀도 (소수점 반올림된 float)
                * "Recall": 재현율 (소수점 반올림된 float)
                * "mAP50": mAP50 (소수점 반올림된 float)
                * "mAP50-95": mAP50-95 (소수점 반올림된 float)
                * "F1 Score": F1 스코어 (소수점 반올림된 float)
    Notes
    -----
    - 이 함수는 각 모델 파일 경로를 기반으로 YOLO 객체를 생성하고, coco128.yaml 데이터셋으로 평가를 진행합니다.
    - 평가 결과는 프로젝트 이름 "test"와 모델 이름 ("A" 또는 "B")로 저장됩니다.
    """

    results_list = []
    model_path_list = [model_a, model_b]
    PROJECT = "test"

    for idx, path in enumerate(model_path_list):
        if idx == 0:
            name = "A"
        else:
            name = "B"

        model = YOLO(path)
        val_results = model.val(project=PROJECT, name=name, data="coco128.yaml", imgsz=640, verbose=False)
        
        # 메트릭 추출
        results_dict = val_results.results_dict
        precision, recall, map50, map5095 = [results_dict[key] for key in val_results.keys]
        
        # F1 Score 계산
        denominator = precision + recall
        f1_score = np.divide(2 * precision * recall, denominator, out=np.zeros_like(denominator), where=denominator!=0)

        # 소수점 반올림
        metrics_array = np.array([precision, recall, map50, map5095, f1_score])
        rounded_metrics = np.round(metrics_array, 4)
        
        # 클래스별 mAP 데이터 추출
        maps = val_results.box.maps  # 클래스별 mAP 점수
        ap_class_index = val_results.box.ap_class_index  # 검출된 클래스 인덱스
        names = val_results.names  # 클래스 이름 딕셔너리
        maps_rounded = np.round(maps, 4) # 소수점 반올림
        
        # 클래스별 메트릭 딕셔너리 생성
        class_metrics = {}
        if len(ap_class_index) > 0:
            for j, class_idx in enumerate(ap_class_index):
                class_name = names[class_idx]
                class_metrics[class_name] = [class_idx, maps_rounded[j]]
        
        # 결과 딕셔너리 생성 - 미리 계산된 값 사용
        result_dict = {
            "Model": path,
            "Metrics": {
                "Precision": rounded_metrics[0],
                "Recall": rounded_metrics[1],
                "mAP50": rounded_metrics[2],
                "mAP50-95": rounded_metrics[3],
                "F1 Score": rounded_metrics[4]
            },
        }
        results_list.append(result_dict)

    return results_list

def model_comparison(model_a_path: str, model_b_path: str, verbose: bool = False, debug: bool = False):
    """
    모델 성능 비교 함수.

    이 함수는 사전에 정의된 테스트 데이터와 메트릭을 활용하여 두 객체 탐지 모델의 성능을 비교합니다.
    각 모델의 주요 성능 지표를 테이블 형식으로 정리하고, 각 메트릭별 우승 모델을 결정한 후,
    전반적인 우승 모델을 가리킵니다. 테이블과 최종 결과는 콘솔에 출력되며, 종합 우승 모델의
    절대 파일 경로가 반환됩니다.

    Parameters
    ----------
    model_a : any
        첫 번째 모델을 나타내는 파라미터입니다.
    model_b : any
        두 번째 모델을 나타내는 파라미터입니다.
    verbose : bool, optional
        상세한 정보를 출력할지 여부를 결정하는 파라미터입니다. 기본값은 False입니다.
    is_test : bool, optional
        테스트 데이터를 사용할지 여부를 결정하는 파라미터입니다. 기본값은 False입니다.
    
    Returns
    -------
    results: list of dict
        각 모델에 대한 평가 결과를 담은 딕셔너리들의 리스트.
    """

    COL_NAMES = ["Metric", "Model A", "Model B", "Result"]
    COL_STYLES = ["cyan", "magenta", "green", "yellow"]
    SUMMARY_ROW = "종합 결과"
    WIN_FORMAT = "최고 메트릭 수: {}개"
    FINAL_RESULT = "종합 최고 모델: {} ({})"
    
    # 테스트 데이터
    if debug:
        test_data = [
            {
                'Model': 'YOLOv8/0/weights/best.pt',
                'Metrics': {
                    'Precision': 0.8995,
                    'Recall': 0.8111,
                    'mAP50': 0.885,
                    'mAP50-95': 0.7231,
                    'F1 Score': 0.853
                }
            },
            {
                'Model': 'YOLOv8/1/weights/best.pt',
                'Metrics': {
                    'Precision': 0.9354,
                    'Recall': 0.8401,
                    'mAP50': 0.9171,
                    'mAP50-95': 0.787,
                    'F1 Score': 0.8852
                }
            }
        ]
        results_list = test_data
    else:
        results_list = ab_test(model_a_path, model_b_path)

    model_a_path = results_list[0]['Model']
    model_b_path = results_list[1]['Model']
    model_a_abs_path = os.path.abspath(model_a_path)
    model_b_abs_path = os.path.abspath(model_b_path)
    
    # 테이블 생성
    if verbose:
        metritable = Table(title="모델 비교 결과")
        for name, style in zip(COL_NAMES, COL_STYLES):
            metric_table.add_column(name, style=style)
    
    # 메트릭 비교
    wins = [0, 0]  # [model_a_wins, model_b_wins]
    
    for metric in results_list[0]['Metrics'].keys():
        a_value = results_list[0]['Metrics'][metric]
        b_value = results_list[1]['Metrics'][metric]
        
        winner = "Model A" if a_value > b_value else "Model B"
        wins[0 if winner == "Model A" else 1] += 1
        
        if verbose:
            metric_table.add_row(
                metric,
                f"{a_value:.4f}",
                f"{b_value:.4f}",
                winner
            )
    
    # 종합 결과
    overall_winner = "Model A" if wins[0] > wins[1] else "Model B"
    winner_path = model_a_abs_path if overall_winner == "Model A" else model_b_abs_path
    
    if verbose:
        console.line()
        console.print("Model A:", model_a_abs_path)
        console.print("Model B:", model_b_abs_path)
        console.line()
        metric_table.add_section()
        
        metric_table.add_row(
            SUMMARY_ROW,
            WIN_FORMAT.format(wins[0]),
            WIN_FORMAT.format(wins[1]),
            overall_winner
        )
        
        console.print(metric_table)
        console.print(FINAL_RESULT.format(overall_winner, winner_path))
        console.line()
    
    comparison_result = {
        "Comparison": {
            "Model A": {
                "Wins": wins[0]
            },
            "Model B": {
                "Wins": wins[1]
            },
            "Winner": winner_path
        }
    }
    results_list.append(comparison_result)
    return results_list

if __name__ == "__main__":
    model_a = "YOLOv8/0/weights/best.pt"
    model_b = "YOLOv8/1/weights/best.pt"

    # results_list = ab_test(model_a, model_b)
    # json_str = json.dumps(results_list, cls=NumpyEncoder)
    # console.print_json(json_str)
    model_comparison(model_a, model_b, True)