import logging
import subprocess
import textwrap
import src.train_yolo as train_yolo
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
import os
# 로깅 설정
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"  

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
LOGGER = logging.getLogger(__name__)

def pt_to_onnx(pt_path: Path, device: int = 0):
    """
    PyTorch .pt 모델을 ONNX 형식으로 변환하고 메타데이터를 반환합니다.

    Parameters
    ----------
    pt_path : pathlib.Path
        변환할 .pt 모델 파일의 경로입니다.
    device : int, optional
        변환에 사용할 GPU 디바이스 인덱스 (기본값: 0).

    Returns
    -------
    onnx_path : pathlib.Path
        출력된 ONNX 모델 파일의 경로입니다.
    metadata : dict
        변환 시 수집된 메타데이터 (모델 정보, 학습 파라미터 등).
    """
    model = YOLO(pt_path)
    metadata = {}
    model.add_callback("on_export_end", lambda exporter: metadata.update(exporter.metadata))
    onnx_path = Path(model.export(format="onnx", dynamic=True, device=device))
    return onnx_path, metadata

def onnx_to_trt(onnx_path: Path, plan_path: Path, device: int = 0, shapes=(1, 3, 10)):
    """
    ONNX 모델을 TensorRT engine(.plan)으로 변환합니다.

    Parameters
    ----------
    onnx_path : pathlib.Path
        입력 ONNX 모델 파일의 경로입니다.
    plan_path : pathlib.Path
        생성할 TensorRT plan 파일의 경로입니다.
    device : int, optional
        TensorRT 빌드에 사용할 GPU 디바이스 인덱스 (기본값: 0).
    shapes : tuple of int, optional
        동적 배치 크기 (min_batch, opt_batch, max_batch).

    Returns
    -------
    pathlib.Path
        생성된 TensorRT plan 파일의 경로를 반환합니다.

    Raises
    ------
    FileNotFoundError
        trtexec 실행 후 plan 파일이 생성되지 않으면 예외를 발생시킵니다.
    """
    min_b, opt_b, max_b = shapes
    cmd = [
        "/usr/src/tensorrt/bin/trtexec",
        f"--onnx={onnx_path}", f"--saveEngine={plan_path}",
        f"--device={device}", "--inputIOFormats=fp16:chw", "--outputIOFormats=fp16:chw", "--fp16",
        f"--minShapes=images:{min_b}x3x640x640",
        f"--optShapes=images:{opt_b}x3x640x640",
        f"--maxShapes=images:{max_b}x3x640x640",
    ]
    LOGGER.info("Executing: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)
    plan_path = Path(plan_path)
    if not plan_path.exists():
        raise FileNotFoundError(f"Failed to create TRT plan: {plan_path}")
    print(plan_path)
    return plan_path

def create_triton_repo(repo_root: Path, save_path: str, plan_path: Path, metadata: dict,
                        batch_sizes=(1, 3, 10), device: int = 0):
    """
    Triton Inference Server용 모델 레포지토리를 생성합니다.

    Parameters
    ----------
    repo_root : pathlib.Path
        Triton 모델 레포지토리의 루트 경로입니다.
    save_path : str
        생성할 모델 디렉토리 이름입니다.
    plan_path : pathlib.Path
        TensorRT engine 파일(.plan)의 경로입니다.
    metadata : dict
        config.pbtxt에 삽입할 모델 메타데이터 딕셔너리입니다.
    batch_sizes : tuple of int, optional
        동적 배칭에서 사용할 배치 크기 목록 [min, opt, max] (기본값: (1,3,10)).
    device : int, optional
        instance_group에 사용할 GPU 디바이스 인덱스 (기본값: 0).
    """
    # 모델 버전 디렉토리 생성
    model_dir = repo_root / save_path / "1"
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / "model.plan").write_bytes(plan_path.read_bytes())

    classes = len(metadata.get('names', [])) + 4
    config_path = repo_root / save_path / "config.pbtxt"
    definition_section = textwrap.dedent(f"""
        name: "{save_path}"
        platform: "tensorrt_plan"
        max_batch_size: {batch_sizes[-1]}
    """).strip()

    input_section = textwrap.dedent(f"""
        input [
            {{
                name: "images"
                data_type: TYPE_FP16
                dims: [3, 640, 640]
            }}
        ]
    """).strip()

    output_section = textwrap.dedent(f"""
        output [
            {{
                name: "output0"
                data_type: TYPE_FP16
                dims: [{classes}, -1]
            }}
        ]
    """).strip()

    dynamic_batching_section = textwrap.dedent(f"""
        dynamic_batching {{ 
            preferred_batch_size: [1, 3, 10]
            max_queue_delay_microseconds: 100                      
        }}
    """).strip()

    instance_group_section = textwrap.dedent(f"""
        instance_group [
            {{
                count: 1
                kind: KIND_GPU
                gpus: {device}
            }}
        ]
    """).strip()
    
    parameters_section = textwrap.dedent(f"""
        parameters {{
            key: "metadata"
            value: {{
                string_value: "{metadata}"
            }}
        }}""").strip()
    
    data = "\n".join([definition_section, input_section, output_section, dynamic_batching_section, instance_group_section, parameters_section])
    with open(config_path, "w") as f:
        f.write(data)
    LOGGER.info(f"Triton repository created: {model_dir}")

#2025.05.23 수정 (박보은)
def main(model_name, pt_path):
    """
    전체 워크플로우를 수행합니다:
      1. .pt → ONNX 변환
      2. ONNX → TensorRT plan 변환
      3. Triton 모델 레포지토리 생성
    """
    
    home_dir = str(Path.home())
    print(f'home_dir:{home_dir}')
    # repo_path = Path(str(home_dir)+"/yolo-triton/tmp/triton_repo") # TEST Com 용
    repo_path = Path(str(home_dir)+"/rist-ai-cctv/tmp/triton_repo") # RIST Com 용
    # save_path = str(pt_path.stem) # yolov8m
    save_path = f"{model_name}"
    onnx_model, metadata = pt_to_onnx(pt_path)
    print(f'onnx_model: {onnx_model}')
    plan_model = onnx_to_trt(onnx_model, pt_path.with_suffix('.plan'))
    print(f'plan_model: {plan_model}')
    create_triton_repo(repo_path, save_path, plan_model, metadata)
    return save_path
if __name__ == "__main__":
    main()
