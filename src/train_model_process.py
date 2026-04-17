# 2025.05.21 파일 추가 (박보은)
import os, sys, yaml, re
# from ultralytics import YOLO 전에 선언 필요
# GPU 0번과 1번만 사용할 수 있도록 환경을 제한
# 재학습 때 다중 GPU 사용하기 위해 필요
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"  

import pandas as pd

from datetime import datetime
from typing import List
from ultralytics import YOLO
from pathlib import Path
# str → bool 변환
def str2bool(s):
    return s.lower() in ("true", "1", "yes")

# str에서 날짜 패턴 제거(정규식 이용, 언더스코어 포함)
def extract_model_prefix(model_path: str) -> str:
    stem = Path(model_path).stem
    match = re.search(r'_\d{8}_\d{6}$', stem)
    if match:
        return stem[:match.start()]  # 날짜 앞까지 자르기
    return stem

def get_last_epoch(model_dir: str) -> int:
    results_path = Path(model_dir) / "results.csv"
    if not results_path.exists():
        return -1
    
    df = pd.read_csv(results_path)
    if df.empty or 'epoch' not in df.columns:
        return -1

    last_epoch = int(df['epoch'].max())  # 다음 에폭 기준으로 반환
    return last_epoch

if __name__ == "__main__":
    try:
        model_name = sys.argv[1]
        retrain_flag = str2bool(sys.argv[3])

        experiment_dir = 'experiments'
        model_dir = f'{experiment_dir}/{model_name}'
        retrain_info_yaml_path = f'{model_dir}/train_info.yaml'

        if retrain_flag and os.path.exists(retrain_info_yaml_path):
            # 설정 불러오기
            with open(retrain_info_yaml_path, 'r') as f:
                retrain_info = yaml.safe_load(f)
            model_path = retrain_info.get('resume')  # default없음
            save_name = retrain_info.get('trained_model')

            dir_path, filename = os.path.split(model_path)
            best_model_path = f"{dir_path}/best.pt"

            # 학습 중단 모델 존재
            if os.path.exists(model_path):
                last_epoch = get_last_epoch(dir_path)
                target_epochs = retrain_info.get('epochs', 0)
                print(f"✅ Found checkpoint. Completed epochs: {last_epoch}/{target_epochs}")
                # 이어하기
                if last_epoch < target_epochs:
                    print("🔁 Resuming training...")
                    model = YOLO(model_path)
                    model.train(resume=True, epochs=target_epochs)
            # 미존재
            else:
                raise FileNotFoundError("학습 중단 모델이 존재하지 않습니다. 파일이 삭제되었거나, 학습 시작 전에 학습 중단 되었을 수 있습니다.")
        else:
            dataset_config_file_path = sys.argv[2]

            # 설정 불러오기
            with open(dataset_config_file_path, 'r') as f:
                dataset_config = yaml.safe_load(f)
            target_epochs = dataset_config.get('epochs', 10)
            save_period = dataset_config.get('save_period', -1)

            model_path = f"{model_dir}/weights/best.pt"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_name = f"{extract_model_prefix(model_name)}_{timestamp}"

            info = {
                'trained_model': save_name, # 학습된 or 중단된 모델 이름
                'project': experiment_dir,
                'data': dataset_config_file_path,
                'epochs': target_epochs,
                'resume': f"{experiment_dir}/{save_name}/weights/last.pt"
            }
            with open(retrain_info_yaml_path, 'w') as f:
                yaml.dump(info, f)

            print("🆕 Starting new training...")
            model = YOLO(model_path)
            model.train(
                data=dataset_config_file_path,
                epochs=target_epochs,
                imgsz=640,
                project=experiment_dir,
                name=save_name,
                exist_ok=True,  # 덮어쓰기 허용
                save=True,      # 체크 포인트 및 가중치 파일 저장 사용 여부
                save_period=save_period,  # 저장 빈도 (epochs), -1 : 비활성화
                device="cpu",  # 다중 GPU 사용
                # device=",".join(map(str, [0,1])) # 학습의 경우 다중 GPU 사용시 오류 발생
            )
            best_model_path = f"{experiment_dir}/{save_name}/weights/best.pt"

        print(f"model save name: {save_name}")
        print(f"Best model saved at: {best_model_path}")
        
    except Exception as e:
        print(f"모델 훈련 오류: {e}")
        raise
