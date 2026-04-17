import os
import mlflow
from dotenv import load_dotenv
from mlflow.tracking import MlflowClient
from rich.traceback import install
from rich.console import Console
install()
console = Console()

class MLflowManager:
    """YOLO 모델 훈련을 MLflow 추적과 함께 관리하는 클래스"""
    
    def __init__(self, experiment_name: str = "YOLOv8"):
        load_dotenv(verbose=False)
        self.mlflow_uri = os.getenv("MLFLOW_URI")
        self.experiment_name = experiment_name
    
    def initialize_client(self) -> None:
        self.mlflow_client  = MlflowClient(tracking_uri=self.mlflow_uri)
        mlflow.set_tracking_uri(uri=self.mlflow_uri)
        
        # 실험 가져오기 또는 생성
        current_experiment = self.mlflow_client.get_experiment_by_name(self.experiment_name)
        """
        current_experiment.to_proto 예시 출력

        experiment_id: "593910773673328784"
        name: "YOLOv8"
        artifact_location: "mlflow-artifacts:/593910773673328784"
        lifecycle_stage: "active"
        last_update_time: 1742193206654
        creation_time: 1742193206654
        """

        experiment_runs = self.mlflow_client.search_runs(experiment_ids=[current_experiment.experiment_id])
        """
        experiment_runs[0].info --> RunInfo 객체 출력
        <RunInfo: 
            artifact_uri='mlflow-artifacts:/593910773673328784/59b179b3f4864fac9270843a15ea06e7/artifacts', 
            end_time=1742195215079, 
            experiment_id='593910773673328784', 
            lifecycle_stage='active', 
            run_id='59b179b3f4864fac9270843a15ea06e7', 
            run_name='1', 
            run_uuid='59b179b3f4864fac9270843a15ea06e7', 
            start_time=1742194839984, 
            status='FINISHED', 
            user_id='skysys'
        >

        experiment_runs[0].to_dictionary() --> RunInfo 객체 상세정보 딕셔너리 출력
        {
            'info': {
            'artifact_uri': 'mlflow-artifacts:/593910773673328784/59b179b3f4864fac9270843a15ea06e7/artifacts',
            'end_time': 1742195215079,
            'experiment_id': '593910773673328784',
            'lifecycle_stage': 'active',
            'run_id': '59b179b3f4864fac9270843a15ea06e7',
            'run_name': '1',
            'run_uuid': '59b179b3f4864fac9270843a15ea06e7',
            'start_time': 1742194839984,
            'status': 'FINISHED',
            'user_id': 'skysys'
            },
            'data': {
            'metrics': {
                'lr/pg0': 1.7790500000000008e-06,
                'lr/pg1': 1.7790500000000008e-06,
                'lr/pg2': 1.7790500000000008e-06,
                'train/box_loss': 0.79014,
                'train/dfl_loss': 0.95422,
                'train/cls_loss': 0.65948,
                'metrics/precisionB': 0.9187163956277692,
                'metrics/recallB': 0.8480990391717721,
                'metrics/mAP50-95B': 0.7862740640741444,
                'metrics/mAP50B': 0.9161938692406175,
                'val/box_loss': 0.65745,
                'val/dfl_loss': 0.88298,
                'val/cls_loss': 0.48585
            },
            'params': {
                'show_conf': 'True',
                'save': 'True',
                'data': '/home/skysys/yolo-mlflow/venv/lib/python3.12/site-packages/ultralytics/cfg/datasets/coco128.yaml',
                'embed': 'None',
                'cache': 'False',
                'translate': '0.1',
                'show': 'False',
                'exist_ok': 'False',
                'int8': 'False',
                'tracker': 'botsort.yaml',
                'conf': 'None',
                'save_json': 'False',
                'perspective': '0.0',
                'box': '7.5',
                'optimizer': 'auto',
                'time': 'None',
                'source': 'None',
                'multi_scale': 'False',
                'lrf': '0.01',
                'task': 'detect',
                'stream_buffer': 'False',
                'max_det': '300',
                'resume': 'False',
                'augment': 'False',
                'profile': 'False',
                'mixup': '0.0',
                'optimize': 'False',
                'kobj': '1.0',
                'close_mosaic': '10',
                'amp': 'True',
                'plots': 'True',
                'fraction': '1.0',
                'nms': 'False',
                'cos_lr': 'False',
                'rect': 'False',
                'simplify': 'True',
                'dynamic': 'False',
                'nbs': '64',
                'hsv_v': '0.4',
                'verbose': 'True',
                'freeze': 'None',
                'opset': 'None',
                'save_dir': 'YOLOv8/1',
                'copy_paste_mode': 'flip',
                'workspace': 'None',
                'epochs': '200',
                'mosaic': '1.0',
                'save_conf': 'False',
                'dfl': '1.5',
                'split': 'val',
                'cls': '0.5',
                'name': '1',
                'save_hybrid': 'False',
                'deterministic': 'True',
                'mask_ratio': '4',
                'val': 'True',
                'hsv_s': '0.7',
                'crop_fraction': '1.0',
                'imgsz': '640',
                'save_crop': 'False',
                'iou': '0.7',
                'model': 'yolov8n.pt',
                'project': 'YOLOv8',
                'dropout': '0.0',
                'overlap_mask': 'True',
                'show_labels': 'True',
                'half': 'False',
                'show_boxes': 'True',
                'keras': 'False',
                'line_width': 'None',
                'batch': '16',
                'mode': 'train',
                'save_period': '-1',
                'pretrained': 'True',
                'degrees': '0.0',
                'agnostic_nms': 'False',
                'dnn': 'False',
                'momentum': '0.937',
                'copy_paste': '0.0',
                'auto_augment': 'randaugment',
                'device': '[0, 1]',
                'warmup_bias_lr': '0.0',
                'flipud': '0.0',
                'single_cls': 'False',
                'warmup_epochs': '3.0',
                'save_txt': 'False',
                'format': 'torchscript',
                'shear': '0.0',
                'pose': '12.0',
                'weight_decay': '0.0005',
                'classes': 'None',
                'retina_masks': 'False',
                'patience': '100',
                'visualize': 'False',
                'bgr': '0.0',
                'scale': '0.5',
                'erasing': '0.4',
                'fliplr': '0.5',
                'cfg': 'None',
                'seed': '0',
                'warmup_momentum': '0.8',
                'hsv_h': '0.015',
                'workers': '8',
                'vid_stride': '1',
                'lr0': '0.01',
                'save_frames': 'False'
            },
            'tags': {
                'mlflow.source.type': 'LOCAL',
                'mlflow.user': 'skysys',
                'mlflow.runName': '1',
                'mlflow.source.name': '/home/skysys/.config/Ultralytics/DDP/_temp_xqfmk5f8133597611276960.py'
            }
            },
            'inputs': {
            'dataset_inputs': []
            }
        }
        """
        console.print(experiment_runs[0].data.metrics)

def main():
    """트레이너를 생성하고 훈련을 시작하는 메인 함수"""
    experiment_name = "YOLOv8"
    mlflow_manager = MLflowManager(experiment_name)
    mlflow_manager.initialize_client()

if __name__ == "__main__":
    main()