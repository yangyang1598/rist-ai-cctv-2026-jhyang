import os
import mlflow
from typing import Optional, List
from dotenv import load_dotenv
from mlflow.tracking import MlflowClient
from ultralytics import YOLO, settings

class YOLOTrainer:
    """YOLO 모델 훈련을 MLflow 추적과 함께 관리하는 클래스"""
    
    def __init__(self, experiment_name: str = "YOLOv8"):
        """
        YOLOTrainer 초기화
        
        Args:
            mlflow_uri: MLflow 추적 서버 URI
            experiment_name: MLflow 실험 이름
        """
        load_dotenv(verbose=False)
        self.mlflow_uri = os.getenv("MLFLOW_URI")
        self.experiment_name = experiment_name
        self.setup_mlflow()
    
    def setup_mlflow(self) -> None:
        """MLflow 클라이언트 및 실험 구성"""
        try:
            self.client = MlflowClient(tracking_uri=self.mlflow_uri)
            mlflow.set_tracking_uri(uri=self.mlflow_uri)
            
            # 실험 가져오기 또는 생성
            experiment = self.client.get_experiment_by_name(self.experiment_name)
            if experiment and experiment.lifecycle_stage == "deleted":
                self.client._tracking_client.restore_experiment(experiment.experiment_id)
            
            mlflow.set_experiment(self.experiment_name)
            settings.update({"mlflow": True})  # Ultralytics에서 MLflow 활성화
        except Exception as e:
            print(f"MLflow 설정 오류: {e}")
            raise
    
    def get_next_run_number(self) -> int:
        """실험을 위한 다음 실행 번호 가져오기"""
        if not os.path.exists(self.experiment_name):
            return 0
        
        existing_runs = [
            d for d in os.listdir(self.experiment_name)
            if os.path.isdir(os.path.join(self.experiment_name, d)) and d.isdigit()
        ]
        
        return max(map(int, existing_runs), default=-1) + 1
    
    def train_model(
        self, 
        model_path: str = "yolov8n.pt",
        data_path: str = "coco128.yaml",
        epochs: int = 200,
        img_size: int = 640,
        devices: List[int] = [0, 1],
        run_name: Optional[str] = None
    ) -> None:
        """
        YOLO 모델 훈련
        
        Args:
            model_path: YOLO 모델 경로
            data_path: 데이터셋 구성 경로
            epochs: 훈련 에포크 수
            img_size: 훈련용 이미지 크기
            devices: 사용할 GPU 장치 목록
            run_name: 이 실행의 이름 (None이면 자동 증가 번호 사용)
        """
        try:
            if run_name is None:
                run_name = str(self.get_next_run_number())
            
            model = YOLO(model_path)
            model.train(
                project=self.experiment_name,
                name=run_name,
                data=data_path,
                epochs=epochs,
                imgsz=img_size,
                device=",".join(map(str, devices))
            )
            best_model_path = f"{self.experiment_name}/{run_name}/weights/best.pt"
            print(f"Best model saved at: {best_model_path}")
            return best_model_path
            
        except Exception as e:
            print(f"모델 훈련 오류: {e}")
            raise


def main():
    """트레이너를 생성하고 훈련을 시작하는 메인 함수"""
    trainer = YOLOTrainer()
    trainer.train_model()

if __name__ == "__main__":
    main()