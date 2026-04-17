import tritonclient.http as httpclient
from typing import List, Dict, Any
from rich.traceback import install
from rich.console import Console
install()
console = Console()


class TritonManager:
    """
    https://github.com/triton-inference-server/server/blob/main/docs/protocol/extension_model_repository.md
    """

    def __init__(self, triton_url: str):
        self.triton_server_url: str = triton_url
        self.triton_client: httpclient.InferenceServerClient = httpclient.InferenceServerClient(url=triton_url)
    
    # def get_model_repository_index(self) -> List[Dict[str, str]]:
    #     """
    #     [
    #         {'name': 'bulti', 'version': '1', 'state': 'READY'},
    #         {'name': 'bulti_ensemble', 'version': '1', 'state': 'READY'},
    #         {'name': 'bulti_ensemble_2', 'version': '1', 'state': 'READY'},
    #         {'name': 'bulti_postprocess', 'version': '1', 'state': 'READY'},
    #         {'name': 'bulti_postprocess_2', 'version': '1', 'state': 'READY'}
    #     ]
    #     """
    #     return self.triton_client.get_model_repository_index()

    # def get_model_metadata(self, model_name: str) -> Dict[str, Any]:
    #     """
    #     {
    #         'name': 'bulti',
    #         'versions': ['1'],
    #         'platform': 'onnxruntime_onnx',
    #         'inputs': [{'name': 'images', 'datatype': 'FP32', 'shape': [-1, 3, 640, 640]}],
    #         'outputs': [{'name': 'output0', 'datatype': 'FP32', 'shape': [-1, 11, -1]}]
    #     }
    #     """
    #     return self.triton_client.get_model_metadata(model_name)

    # def get_model_config(self, model_name: str) -> Dict[str, Any]:
    #     """
    #     {
    #         'name': 'bulti',
    #         'platform': 'onnxruntime_onnx',
    #         'backend': 'onnxruntime',
    #         'runtime': '',
    #         'version_policy': {'latest': {'num_versions': 1}},
    #         'max_batch_size': 1,
    #         'input': [
    #             {
    #                 'name': 'images',
    #                 'data_type': 'TYPE_FP32',
    #                 'format': 'FORMAT_NONE',
    #                 'dims': [3, 640, 640],
    #                 'is_shape_tensor': False,
    #                 'allow_ragged_batch': False,
    #                 'optional': False,
    #                 'is_non_linear_format_io': False
    #             }
    #         ],
    #         'output': [{'name': 'output0', 'data_type': 'TYPE_FP32', 'dims': [11, -1], 'label_filename': '', 'is_shape_tensor': False, 'is_non_linear_format_io': False}],
    #         'batch_input': [],
    #         'batch_output': [],
    #         'optimization': {
    #             'priority': 'PRIORITY_DEFAULT',
    #             'input_pinned_memory': {'enable': True},
    #             'output_pinned_memory': {'enable': True},
    #             'gather_kernel_buffer_threshold': 0,
    #             'eager_batching': False
    #         },
    #         'instance_group': [{'name': 'bulti', 'kind': 'KIND_GPU', 'count': 1, 'gpus': [0, 1], 'secondary_devices': [], 'profile': [], 'passive': False, 'host_policy': ''}],
    #         'default_model_filename': 'model.onnx',
    #         'cc_model_filenames': {},
    #         'metric_tags': {},
    #         'parameters': {
    #             'metadata': {
    #                 'string_value': "{'description': 'Ultralytics bulti model trained on AGT_project_test.yaml', 'author': 'Ultralytics', 'date': '2025-03-10T10:34:50.634779', 'version': '8.3.76', 
    #                 'license': 'AGPL-3.0 License (https://ultralytics.com/license)', 'docs': 'https://docs.ultralytics.com', 'stride': 32, 'task': 'detect', 'batch': 1, 'imgsz': [640, 640], 'names': {0: 'person', 1: 
    #                 'rough_opening', 2: 'sparks', 3: 'safety_hook', 4: 'safety_belt', 5: 'helmet', 6: 'vest'}, 'args': {'batch': 1, 'half': False, 'dynamic': True, 'simplify': True, 'opset': None, 'nms': False}}"
    #             }
    #         },
    #         'model_warmup': []
    #     }
    #     """
    #     return self.triton_client.get_model_config(model_name)

    def __call__(self):
        return self.triton_client
    
if __name__ == "__main__":
    URL, PORT = "192.168.88.24", "8000"
    TRITON_URL = ":".join([URL, PORT])
    manager = TritonManager(TRITON_URL)
    console.print(manager.get_model_repository_index())