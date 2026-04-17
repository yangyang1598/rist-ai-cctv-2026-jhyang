import os
import logging
import textwrap
from pathlib import Path
from ultralytics import YOLO

def convert_pt_to_onnx(model_path):
    # Load a model
    model = YOLO(model_path)  # load an official model

    # Retrieve metadata during export
    metadata = []

    def export_cb(exporter):
        metadata.append(exporter.metadata)

    model.add_callback("on_export_end", export_cb)

    # Export the model
    model_file = model.export(format="onnx", dynamic=True)

    return model_file, metadata

def convert_onnx_to_plan(onnx_file_path, plan_file_path, half=True):
    """
    TRT Plan 파일 변환 예제

    원본 명령어:
    /usr/src/tensorrt/bin/trtexec \
        --onnx=model.onnx \
        --saveEngine=model.plan \
        --inputIOFormats=fp16:chw \
        --outputIOFormats=fp16:chw \
        --fp16 \
        --minShapes=images:1x3x640x640 \
        --maxShapes=images:10x3x640x640 \
        --optShapes=images:3x3x640x640
    """
    result = False

    cmd_parts = ['sudo /usr/src/tensorrt/bin/trtexec']
    cmd_parts.append(f"--onnx={onnx_file_path}")
    cmd_parts.append(f"--saveEngine={plan_file_path}")
    cmd_parts.append(f"--device=1")
    
    # precision 설정
    if half:
        cmd_parts.append("--inputIOFormats=fp16:chw")
        cmd_parts.append("--outputIOFormats=fp16:chw")
        cmd_parts.append("--fp16")
    else:
        cmd_parts.append("--inputIOFormats=fp32:chw")
        cmd_parts.append("--outputIOFormats=fp32:chw")
    
    # 동적 shape 설정
    cmd_parts.append("--minShapes=images:1x3x640x640")
    cmd_parts.append("--maxShapes=images:10x3x640x640")
    cmd_parts.append("--optShapes=images:3x3x640x640")
    
    # 명령어 실행
    cmd = " ".join(cmd_parts)
    logging.info(f"Executing: {cmd}")
    os.system(cmd)
    
    # 결과 확인
    if os.path.isfile(plan_file_path):
        logging.info(f"TRT File has been successfully created: {plan_file_path}")
        result = True
    else:
        logging.warning(f"TRT File has not been successfully created: {plan_file_path}")
        result = False
    return result
    
def create_config_pbtxt(config_path: Path, model_name, platform, batch_size, image_size, classes, metadata):
    config_path.touch()
    platform = "onnxruntime_onnx" if platform == "onnx" else "tensorrt_plan"
    definition_section = textwrap.dedent(f"""
        name: "{model_name}"
        platform: "{platform}"
        max_batch_size: {batch_size}
    """).strip()

    if platform == "tensorrt_plan":
        input_section = textwrap.dedent(f"""
            input [
                {{
                    name: "images"
                    data_type: TYPE_FP16
                    dims: [3, 640, 640]
                }}
            ]
        """).strip()

    else:
        input_section = textwrap.dedent(f"""
            input [
                {{
                    name: "images"
                    data_type: TYPE_FP32
                    dims: [-1, 3, -1, -1]
                }}
            ]
        """).strip()

    if platform == "tensorrt_plan":
        output_section = textwrap.dedent(f"""
            output [
                {{
                    name: "output0"
                    data_type: TYPE_FP16
                    dims: [{classes}, -1]
                }}
            ]
        """).strip()
    else:
        output_section = textwrap.dedent(f"""
            output [
                {{
                    name: "output0"
                    data_type: TYPE_FP32
                    dims: [-1, {classes}, -1]
                }}
            ]
        """).strip()

    if platform == "tensorrt_plan":
        dynamic_batching_section = textwrap.dedent(f"""
            dynamic_batching {{ 
                preferred_batch_size: [1, 3, 10]
                max_queue_delay_microseconds: 100                      
            }}
        """).strip()
    else:
        dynamic_batching_section = textwrap.dedent(f"""
            dynamic_batching {{ }}
        """).strip()

    if platform == "tensorrt_plan":
        pass
    else:
        instance_group_section = textwrap.dedent(f"""
            instance_group [
                {{
                    count: 4
                    kind: KIND_GPU
                    gpus: [0, 1]
                }}
            ]
        """).strip()
    
    parameters_section = textwrap.dedent(f"""
        parameters {{
            key: "metadata"
            value: {{
                string_value: "{metadata[0]}"
            }}
        }}""").strip()
    
    data = "\n".join([definition_section, input_section, output_section, dynamic_batching_section, instance_group_section, parameters_section])

    with open(config_path, "w") as f:
        f.write(data)
    logging.info(f"컨픽 생성 완료: {config_path}")

def create_model_repository(model_dir: Path, version: int, model_file: str, platform: str, triton_model_path: Path):
    # Find the next available version
    while model_dir.exists():
        version += 1
        model_dir = triton_model_path / str(version)

    # Create directories
    model_dir.mkdir(parents=True, exist_ok=True)

    # Move ONNX model to Triton Model path
    model_name = "model.onnx"
    if platform == "plan":
        model_name = "model.plan"

    Path(model_file).rename(model_dir / model_name)
    logging.info(f"모델 생성 완료: {model_dir}")

def create_model_repository_workflow(model_path: str, metadata: list, model_name: str, triton_repo_path: str):
    platform = model_path.split(".")[-1] # ex) onnx
    if platform == "onnx":
        batch_size = 0
    else:
        batch_size = 10
    image_size = metadata[0]["imgsz"] # ex) [640, 640]
    classes = len(metadata[0]["names"]) + 4 # "number of classes + 4" accounts for both the class probabilities and the four bounding box regression values (x, y, width, height) ex) YOLOv8s -> 84 (80 class + 4)
    initial_version = 1
    logging.info("==================== TensorRT Plan Convert ====================")
    logging.info(f"Model Path: {model_path}")
    logging.info(f"Metadata: {metadata}")
    logging.info(f"Model Name: {model_name}")
    logging.info(f"Platform: {platform}")
    logging.info(f"Batch Size: {batch_size}")
    logging.info(f"Image Size: {image_size}")
    logging.info(f"Classes: {classes}")
    logging.info(f"Initial Version: {initial_version}")
    logging.info(f"Triton Repo Path: {triton_repo_path}")

    # Define paths
    triton_model_path: Path = Path(triton_repo_path) / model_name # /home/skysys/yolo-triton/tmp/triton_repo/triton_repo/test
    version = initial_version
    model_dir = triton_model_path / str(version)

    # Create model repository
    create_model_repository(model_dir, version, model_path, platform, triton_model_path)

    # Create config file
    config_path = (triton_model_path / "config.pbtxt")
    if not config_path.exists():
        create_config_pbtxt(config_path, model_name, platform, batch_size, image_size, classes, metadata)