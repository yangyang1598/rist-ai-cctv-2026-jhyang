# RIST AI CCTV-2025 2nd


## 역할 (Role & Responsibility)
### Application : 개발팀, 이승렬 
Wigdet - SafetyEventLog

SafetyEventLog:Widget()
safetyevent_click:qtsignal( SafetyEventLogData )


### 분석 및 시각화 : 박동현 연구원
Widget - VideoPlayer

ex> 
VideoPlayer:Widget(rtsp_url, triton_url)

play()
stop()

signal-slot
detect_object:qtsignal (bbox, class)


## 스레드 관리
각 스레드 방식별 장단점, 특성, 개별 스터디


## 일정
- 6월 4일 RIST 시연
- 6월 중순 서버 납품
- 6월 중순 대여 서버 반납
- 7월 지능형 CCTV 구동



이 프로그램의 타이틀 아이콘 main_icon.ico은 Flaticon.com의 자료를 사용해 디자인되었습니다.
<a href="https://www.flaticon.com/kr/free-icons/cctv-" title="cctv 카메라 아이콘">Cctv 카메라 아이콘 제작자: Anggre Tionanda - Flaticon</a>


## 에러 로그
### tensorrt


1. CLI 명령어
/usr/src/tensorrt/bin/trtexec --onnx=/home/rist/rist-ai-cctv-2025-2nd/experiments/a_20250617_184317/weights/best.onnx --saveEngine=/home/rist/rist-ai-cctv-2025-2nd/experiments/a_20250617_184317/weights/best.plan --device=1 --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16 --minShapes=images:1x3x640x640 --optShapes=images:3x3x640x640 --maxShapes=images:10x3x640x640

```bash
&&&& PASSED TensorRT.trtexec [TensorRT v100800] [b43] # /usr/src/tensorrt/bin/trtexec --onnx=/home/rist/rist-ai-cctv-2025-2nd/experiments/a_20250617_184317/weights/best.onnx --saveEngine=/home/rist/rist-ai-cctv-2025-2nd/experiments/a_20250617_184317/weights/best.plan --device=1 --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16 --minShapes=images:1x3x640x640 --optShapes=images:3x3x640x640 --maxShapes=images:10x3x640x640
```

2. 실패 로그
```bash
home_dir:/home/rist
Ultralytics 8.3.149 🚀 Python-3.12.3 torch-2.7.0+cu128 CUDA:1 (NVIDIA RTX 6000 Ada Generation, 48520MiB)
💡 ProTip: Export to OpenVINO format for best performance on Intel CPUs. Learn more at https://docs.ultralytics.com/integrations/openvino/
Model summary (fused): 72 layers, 11,156,544 parameters, 0 gradients, 28.6 GFLOPs

PyTorch: starting from 'experiments/a_20250617_184317/weights/best.pt' with input shape (1, 3, 640, 640) BCHW and output shape(s) (1, 84, 8400) (21.5 MB)
requirements: Ultralytics requirement ['onnxslim>=0.1.56'] not found, attempting AutoUpdate...

requirements: AutoUpdate success ✅ 0.5s
WARNING ⚠️ requirements: Restart runtime or rerun command for updates to take effect


ONNX: starting export with onnx 1.17.0 opset 19...
ONNX: slimming with onnxslim 0.1.57...
[INFO] Video1 - video_process.py:L270 - [CCTV 2] 위험 상황 감지
[INFO] Video1 - video_process.py:L628 - 비디오 저장 기능은 아직 구현되지 않았습니다.
[WARNING] Video1 - video_process.py:L646 - 출력 큐가 가득 참 - 이벤트 로그 전송 실패
[INFO] Video1 - video_process.py:L592 - 이벤트 로그 생성: EventLogData(timestamp=1750153472.7186983, cctv_location='1공장', cctv_name='CCTV 2', event_name='사람과 차', image_path='/home/rist/rist-ai-cctv-2025-2nd/img/2025-06-17/20250617_184432_CCTV 2.jpg')
ONNX: export success ✅ 5.6s, saved as 'experiments/a_20250617_184317/weights/best.onnx' (42.6 MB)

Export complete (6.8s)
Results saved to /home/rist/rist-ai-cctv-2025-2nd/experiments/a_20250617_184317/weights
Predict:         yolo predict task=detect model=experiments/a_20250617_184317/weights/best.onnx imgsz=640  
Validate:        yolo val task=detect model=experiments/a_20250617_184317/weights/best.onnx imgsz=640 data=/home/rist/rist-ai-cctv-2025-2nd/coco128.yaml  
Visualize:       https://netron.app
onnx_model: experiments/a_20250617_184317/weights/best.onnx
INFO:src.plan_converter:Executing: /usr/src/tensorrt/bin/trtexec --onnx=experiments/a_20250617_184317/weights/best.onnx --saveEngine=experiments/a_20250617_184317/weights/best.plan --device=1 --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16 --minShapes=images:1x3x640x640 --optShapes=images:3x3x640x640 --maxShapes=images:10x3x640x640
&&&& RUNNING TensorRT.trtexec [TensorRT v100800] [b43] # /usr/src/tensorrt/bin/trtexec --onnx=experiments/a_20250617_184317/weights/best.onnx --saveEngine=experiments/a_20250617_184317/weights/best.plan --device=1 --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16 --minShapes=images:1x3x640x640 --optShapes=images:3x3x640x640 --maxShapes=images:10x3x640x640
[06/17/2025-18:44:33] [I] === Model Options ===
[06/17/2025-18:44:33] [I] Format: ONNX
[06/17/2025-18:44:33] [I] Model: experiments/a_20250617_184317/weights/best.onnx
[06/17/2025-18:44:33] [I] Output:
[06/17/2025-18:44:33] [I] === Build Options ===
[06/17/2025-18:44:33] [I] Memory Pools: workspace: default, dlaSRAM: default, dlaLocalDRAM: default, dlaGlobalDRAM: default, tacticSharedMem: default
[06/17/2025-18:44:33] [I] avgTiming: 8
[06/17/2025-18:44:33] [I] Precision: FP32+FP16
[06/17/2025-18:44:33] [I] LayerPrecisions: 
[06/17/2025-18:44:33] [I] Layer Device Types: 
[06/17/2025-18:44:33] [I] Calibration: 
[06/17/2025-18:44:33] [I] Refit: Disabled
[06/17/2025-18:44:33] [I] Strip weights: Disabled
[06/17/2025-18:44:33] [I] Version Compatible: Disabled
[06/17/2025-18:44:33] [I] ONNX Plugin InstanceNorm: Disabled
[06/17/2025-18:44:33] [I] TensorRT runtime: full
[06/17/2025-18:44:33] [I] Lean DLL Path: 
[06/17/2025-18:44:33] [I] Tempfile Controls: { in_memory: allow, temporary: allow }
[06/17/2025-18:44:33] [I] Exclude Lean Runtime: Disabled
[06/17/2025-18:44:33] [I] Sparsity: Disabled
[06/17/2025-18:44:33] [I] Safe mode: Disabled
[06/17/2025-18:44:33] [I] Build DLA standalone loadable: Disabled
[06/17/2025-18:44:33] [I] Allow GPU fallback for DLA: Disabled
[06/17/2025-18:44:33] [I] DirectIO mode: Disabled
[06/17/2025-18:44:33] [I] Restricted mode: Disabled
[06/17/2025-18:44:33] [I] Skip inference: Disabled
[06/17/2025-18:44:33] [I] Save engine: experiments/a_20250617_184317/weights/best.plan
[06/17/2025-18:44:33] [I] Load engine: 
[06/17/2025-18:44:33] [I] Profiling verbosity: 0
[06/17/2025-18:44:33] [I] Tactic sources: Using default tactic sources
[06/17/2025-18:44:33] [I] timingCacheMode: local
[06/17/2025-18:44:33] [I] timingCacheFile: 
[06/17/2025-18:44:33] [I] Enable Compilation Cache: Enabled
[06/17/2025-18:44:33] [I] Enable Monitor Memory: Disabled
[06/17/2025-18:44:33] [I] errorOnTimingCacheMiss: Disabled
[06/17/2025-18:44:33] [I] Preview Features: Use default preview flags.
[06/17/2025-18:44:33] [I] MaxAuxStreams: -1
[06/17/2025-18:44:33] [I] BuilderOptimizationLevel: -1
[06/17/2025-18:44:33] [I] MaxTactics: -1
[06/17/2025-18:44:33] [I] Calibration Profile Index: 0
[06/17/2025-18:44:33] [I] Weight Streaming: Disabled
[06/17/2025-18:44:33] [I] Runtime Platform: Same As Build
[06/17/2025-18:44:33] [I] Debug Tensors: 
[06/17/2025-18:44:33] [I] Input(s): fp16:chw
[06/17/2025-18:44:33] [I] Output(s): fp16:chw
[06/17/2025-18:44:33] [I] Input build shape (profile 0): images=1x3x640x640+3x3x640x640+10x3x640x640
[06/17/2025-18:44:33] [I] Input calibration shapes: model
[06/17/2025-18:44:33] [I] === System Options ===
[06/17/2025-18:44:33] [I] Device: 1
[06/17/2025-18:44:33] [I] DLACore: 
[06/17/2025-18:44:33] [I] Plugins:
[06/17/2025-18:44:33] [I] setPluginsToSerialize:
[06/17/2025-18:44:33] [I] dynamicPlugins:
[06/17/2025-18:44:33] [I] ignoreParsedPluginLibs: 0
[06/17/2025-18:44:33] [I] 
[06/17/2025-18:44:33] [I] === Inference Options ===
[06/17/2025-18:44:33] [I] Batch: Explicit
[06/17/2025-18:44:33] [I] Input inference shape : images=3x3x640x640
[06/17/2025-18:44:33] [I] Iterations: 10
[06/17/2025-18:44:33] [I] Duration: 3s (+ 200ms warm up)
[06/17/2025-18:44:33] [I] Sleep time: 0ms
[06/17/2025-18:44:33] [I] Idle time: 0ms
[06/17/2025-18:44:33] [I] Inference Streams: 1
[06/17/2025-18:44:33] [I] ExposeDMA: Disabled
[06/17/2025-18:44:33] [I] Data transfers: Enabled
[06/17/2025-18:44:33] [I] Spin-wait: Disabled
[06/17/2025-18:44:33] [I] Multithreading: Disabled
[06/17/2025-18:44:33] [I] CUDA Graph: Disabled
[06/17/2025-18:44:33] [I] Separate profiling: Disabled
[06/17/2025-18:44:33] [I] Time Deserialize: Disabled
[06/17/2025-18:44:33] [I] Time Refit: Disabled
[06/17/2025-18:44:33] [I] NVTX verbosity: 0
[06/17/2025-18:44:33] [I] Persistent Cache Ratio: 0
[06/17/2025-18:44:33] [I] Optimization Profile Index: 0
[06/17/2025-18:44:33] [I] Weight Streaming Budget: 100.000000%
[06/17/2025-18:44:33] [I] Inputs:
[06/17/2025-18:44:33] [I] Debug Tensor Save Destinations:
[06/17/2025-18:44:33] [I] === Reporting Options ===
[06/17/2025-18:44:33] [I] Verbose: Disabled
[06/17/2025-18:44:33] [I] Averages: 10 inferences
[06/17/2025-18:44:33] [I] Percentiles: 90,95,99
[06/17/2025-18:44:33] [I] Dump refittable layers:Disabled
[06/17/2025-18:44:33] [I] Dump output: Disabled
[06/17/2025-18:44:33] [I] Profile: Disabled
[06/17/2025-18:44:33] [I] Export timing to JSON file: 
[06/17/2025-18:44:33] [I] Export output to JSON file: 
[06/17/2025-18:44:33] [I] Export profile to JSON file: 
[06/17/2025-18:44:33] [I] 
[06/17/2025-18:44:33] [I] === Device Information ===
[06/17/2025-18:44:33] [I] Available Devices: 
[06/17/2025-18:44:33] [I]   Device 0: "NVIDIA RTX 6000 Ada Generation" UUID: GPU-f19d34a7-f286-3e8d-3cc4-5c99408d52b6
[06/17/2025-18:44:33] [I] Cannot find device ID 1!
```


### DB 연결 안됬을 때 실행하면 아래 에러 발생 후 프로그램 강제 종료

```bash
rist@rist-ai-cctv:~/rist-ai-cctv-2025-2nd$ uv run main_window.py
qt.core.qmetaobject.connectslotsbyname: QMetaObject::connectSlotsByName: No matching signal for on_cctv_list_stream_info_selected(QString)
╭───────────────────── Traceback (most recent call last) ──────────────────────╮
│ /home/rist/rist-ai-cctv-2025-2nd/.venv/lib/python3.12/site-packages/pymysql/ │
│ connections.py:649 in connect                                                │
│                                                                              │
│    646 │   │   │   │   │   │   kwargs["source_address"] = (self.bind_address │
│    647 │   │   │   │   │   while True:                                       │
│    648 │   │   │   │   │   │   try:                                          │
│ ❱  649 │   │   │   │   │   │   │   sock = socket.create_connection(          │
│    650 │   │   │   │   │   │   │   │   (self.host, self.port), self.connect_ │
│    651 │   │   │   │   │   │   │   )                                         │
│    652 │   │   │   │   │   │   │   break                                     │
│                                                                              │
│ /usr/lib/python3.12/socket.py:852 in create_connection                       │
│                                                                              │
│   849 │   if len(exceptions):                                                │
│   850 │   │   try:                                                           │
│   851 │   │   │   if not all_errors:                                         │
│ ❱ 852 │   │   │   │   raise exceptions[0]                                    │
│   853 │   │   │   raise ExceptionGroup("create_connection failed", exception │
│   854 │   │   finally:                                                       │
│   855 │   │   │   # Break explicitly a reference cycle                       │
│                                                                              │
│ /usr/lib/python3.12/socket.py:837 in create_connection                       │
│                                                                              │
│   834 │   │   │   │   sock.settimeout(timeout)                               │
│   835 │   │   │   if source_address:                                         │
│   836 │   │   │   │   sock.bind(source_address)                              │
│ ❱ 837 │   │   │   sock.connect(sa)                                           │
│   838 │   │   │   # Break explicitly a reference cycle                       │
│   839 │   │   │   exceptions.clear()                                         │
│   840 │   │   │   return sock                                                │
╰──────────────────────────────────────────────────────────────────────────────╯
TimeoutError: timed out

During handling of the above exception, another exception occurred:

╭───────────────────── Traceback (most recent call last) ──────────────────────╮
│ /home/rist/rist-ai-cctv-2025-2nd/main_window.py:464 in <module>              │
│                                                                              │
│   461 if __name__ == "__main__":                                             │
│   462 │   mp.set_start_method('spawn', force=True)                           │
│   463 │   app = QApplication(sys.argv)                                       │
│ ❱ 464 │   window = MainWindow()                                              │
│   465 │   window.show()                                                      │
│   466 │   window.play_all_cctv_streams(72)                                   │
│   467 │   sys.exit(app.exec())                                               │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/main_window.py:31 in __init__               │
│                                                                              │
│    28 │   │   super().__init__()                                             │
│    29 │   │   self.logger = setup_logger("MainWindow")                       │
│    30 │   │   self.setupUi(self)                                             │
│ ❱  31 │   │   self.setup_ui()                                                │
│    32 │   │   self.init_ui()                                                 │
│    33 │                                                                      │
│    34 │   def setup_ui(self):                                                │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/main_window.py:55 in setup_ui               │
│                                                                              │
│    52 │   │   self.label_cctv_connection_status_widget.deleteLater()         │
│    53 │   │                                                                  │
│    54 │   │   # CCTV 목록                                                    │
│ ❱  55 │   │   self.cctv_list_widget = CctvListWidget()                       │
│    56 │   │   self.layout_left.replaceWidget(self.label_cctv_list_widget, se │
│    57 │   │   self.label_cctv_list_widget.deleteLater()                      │
│    58                                                                        │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/widget/cctv_list_widget.py:27 in __init__   │
│                                                                              │
│    24 │   │   self.button_cctv_search.clicked.connect(self.filter_tree_items │
│    25 │   │   self.line_edit_cctv_search.returnPressed.connect(self.filter_t │
│    26 │   │                                                                  │
│ ❱  27 │   │   self.load_cctv_list_to_tree(self.tree_widget_cctv_list)        │
│    28 │                                                                      │
│    29 │   def load_cctv_list_to_tree(self, tree_widget: QTreeWidget):        │
│    30 │   │   rows = db_cctv_list.get_cctv_list()                            │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/widget/cctv_list_widget.py:30 in            │
│ load_cctv_list_to_tree                                                       │
│                                                                              │
│    27 │   │   self.load_cctv_list_to_tree(self.tree_widget_cctv_list)        │
│    28 │                                                                      │
│    29 │   def load_cctv_list_to_tree(self, tree_widget: QTreeWidget):        │
│ ❱  30 │   │   rows = db_cctv_list.get_cctv_list()                            │
│    31 │   │                                                                  │
│    32 │   │   # 1. 자연 정렬을 위해 장소별 CCTV 저장                         │
│    33 │   │   location_dict = defaultdict(list)                              │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/db/db_cctv_list.py:6 in get_cctv_list       │
│                                                                              │
│     3 def get_cctv_list():                                                   │
│     4 │   sql = "SELECT * FROM camera_list ORDER BY camera_location"         │
│     5 │   db = DBManager()                                                   │
│ ❱   6 │   return db.fetch_all(sql)                                           │
│     7                                                                        │
│     8 def delete_cctv_by_name(name):                                         │
│     9 │   sql = "DELETE FROM camera_list WHERE camera_name = %s"             │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/db/db_manager.py:70 in fetch_all            │
│                                                                              │
│   67 │                                                                       │
│   68 │   def fetch_all(self, sql, params=None):                              │
│   69 │   │   try:                                                            │
│ ❱ 70 │   │   │   with self._get_connection() as conn:                        │
│   71 │   │   │   │   with conn.cursor() as cursor:                           │
│   72 │   │   │   │   │   # print(f'----------------------- FETCH ALL SQL:\n{ │
│   73 │   │   │   │   │   # print(f'----------------------- PARAMS:\n{params} │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/db/db_manager.py:18 in _get_connection      │
│                                                                              │
│   15 │   │   }                                                               │
│   16 │                                                                       │
│   17 │   def _get_connection(self):                                          │
│ ❱ 18 │   │   return pymysql.connect(**self.db_config)                        │
│   19 │                                                                       │
│   20 │   def execute(self, sql, params=None, return_rowcount=False):         │
│   21 │   │   try:                                                            │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/.venv/lib/python3.12/site-packages/pymysql/ │
│ connections.py:361 in __init__                                               │
│                                                                              │
│    358 │   │   if defer_connect:                                             │
│    359 │   │   │   self._sock = None                                         │
│    360 │   │   else:                                                         │
│ ❱  361 │   │   │   self.connect()                                            │
│    362 │                                                                     │
│    363 │   def __enter__(self):                                              │
│    364 │   │   return self                                                   │
│                                                                              │
│ /home/rist/rist-ai-cctv-2025-2nd/.venv/lib/python3.12/site-packages/pymysql/ │
│ connections.py:716 in connect                                                │
│                                                                              │
│    713 │   │   │   │   exc.traceback = traceback.format_exc()                │
│    714 │   │   │   │   if DEBUG:                                             │
│    715 │   │   │   │   │   print(exc.traceback)                              │
│ ❱  716 │   │   │   │   raise exc                                             │
│    717 │   │   │                                                             │
│    718 │   │   │   # If e is neither DatabaseError or IOError, It's a bug.   │
│    719 │   │   │   # But raising AssertionError hides original error.        │
╰──────────────────────────────────────────────────────────────────────────────╯
OperationalError: (2003, "Can't connect to MySQL server on '192.168.88.20' 
(timed out)")
```

### 영상 관련 에러
1. 빈 그리드 셀 없을 때 CCTV 리스트에서 CCTV 클릭 시 KeyError 반복

```bash
[WARNING] VideoPlayerWidget - video_player_widget.py:L130 - No empty cell found.
╭───────────────────── Traceback (most recent call last) ──────────────────────╮
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_process_pipeline/video_player_ │
│ widget.py:266 in on_frame_received                                           │
│                                                                              │
│   263 │   │   │   routing_list = self.frame_routing_table[cctv_id]           │
│   264 │   │   │   for routing_info in routing_list:                          │
│   265 │   │   │   │   target_tab_index = routing_info['target_tab']          │
│ ❱ 266 │   │   │   │   unique_key = routing_info['unique_key']                │
│   267 │   │   │   │   self.frame_routing_requested.emit(cctv_id, target_tab_ │
│   268 │                                                                      │
│   269 │   # 프레임 라우팅 관련 함수                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
KeyError: 'unique_key'
```

2. 원인불명
```bash
[NULL @ 0x46edd9c0] Picture timing SEI payload too large
```

3. 1x1 레이아웃 저장 에러
```bash
╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_layout_widget.py:49 in add_video_layout            │
│                                                                                                  │
│    46 │   │   │   │   layout_name = text.strip()                                                 │
│    47 │   │   │   │                                                                              │
│    48 │   │   │   │   if self.video_player_widget:                                               │
│ ❱  49 │   │   │   │   │   new_video_data = self.find_grid_layout()                               │
│    50 │   │   │   │   │   self.save_video_layout(layout_name, new_video_data)                    │
│    51 │   │   │   │   else:                                                                      │
│    52 │   │   │   │   │   QMessageBox.warning(self, "오류", "비디오 플레이어 위젯이 초기화되지   │
│                                                                                                  │
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_layout_widget.py:57 in find_grid_layout            │
│                                                                                                  │
│    54 │   │   │   │   QMessageBox.warning(self, "입력 오류", "레이아웃 이름을 입력하지 않았습    │
│    55 │                                                                                          │
│    56 │   def find_grid_layout(self):                                                            │
│ ❱  57 │   │   self.video_player_widget.send_current_layout_data()                                │
│    58 │   │   grid_layout = self.video_player_widget.grid_layout                                 │
│    59 │   │   cctv_info = self.current_layout_data.cctv_info                                     │
│    60 │   │   new_video_data = []                                                                │
│                                                                                                  │
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_process_pipeline/video_player_widget.py:313 in     │
│ send_current_layout_data                                                                         │
│                                                                                                  │
│   310 │   │   현재 그리드 정보를 전송합니다.                                                     │
│   311 │   │   """                                                                                │
│   312 │   │   layout_data = LayoutData(                                                          │
│ ❱ 313 │   │   │   row=self.grid_layout.rowCount(),                                               │
│   314 │   │   │   col=self.grid_layout.columnCount(),                                            │
│   315 │   │   │   grid=self.grid_layout,                                                         │
│   316 │   │   │   cctv_info={k: v.cctv_info for k, v in self.video_widgets.items() if isinstan   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
AttributeError: 'NoneType' object has no attribute 'rowCount'
╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_layout_widget.py:49 in add_video_layout            │
│                                                                                                  │
│    46 │   │   │   │   layout_name = text.strip()                                                 │
│    47 │   │   │   │                                                                              │
│    48 │   │   │   │   if self.video_player_widget:                                               │
│ ❱  49 │   │   │   │   │   new_video_data = self.find_grid_layout()                               │
│    50 │   │   │   │   │   self.save_video_layout(layout_name, new_video_data)                    │
│    51 │   │   │   │   else:                                                                      │
│    52 │   │   │   │   │   QMessageBox.warning(self, "오류", "비디오 플레이어 위젯이 초기화되지   │
│                                                                                                  │
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_layout_widget.py:57 in find_grid_layout            │
│                                                                                                  │
│    54 │   │   │   │   QMessageBox.warning(self, "입력 오류", "레이아웃 이름을 입력하지 않았습    │
│    55 │                                                                                          │
│    56 │   def find_grid_layout(self):                                                            │
│ ❱  57 │   │   self.video_player_widget.send_current_layout_data()                                │
│    58 │   │   grid_layout = self.video_player_widget.grid_layout                                 │
│    59 │   │   cctv_info = self.current_layout_data.cctv_info                                     │
│    60 │   │   new_video_data = []                                                                │
│                                                                                                  │
│ /home/rist/rist-ai-cctv-2025-2nd/widget/video_process_pipeline/video_player_widget.py:313 in     │
│ send_current_layout_data                                                                         │
│                                                                                                  │
│   310 │   │   현재 그리드 정보를 전송합니다.                                                     │
│   311 │   │   """                                                                                │
│   312 │   │   layout_data = LayoutData(                                                          │
│ ❱ 313 │   │   │   row=self.grid_layout.rowCount(),                                               │
│   314 │   │   │   col=self.grid_layout.columnCount(),                                            │
│   315 │   │   │   grid=self.grid_layout,                                                         │
│   316 │   │   │   cctv_info={k: v.cctv_info for k, v in self.video_widgets.items() if isinstan   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
AttributeError: 'NoneType' object has no attribute 'rowCount'
```

### AI 모델 관련 에러

1. 모델 로드 실패
```bash
[ERROR] Video4 - video_process.py:L132 - 모델 로드 실패: test_06 - Triton 모델 목록에 없음
[ERROR] Video4 - video_process.py:L132 - 모델 로드 실패: test_06 - Triton 모델 목록에 없음
[ERROR] Video4 - video_process.py:L132 - 모델 로드 실패: test_06 - Triton 모델 목록에 없음
```

2. Triton 추론 요청 실패
```bash
[ERROR] Video21 - video_process.py:L360 - 감지 루프 오류: [StatusCode.NOT_FOUND] Request for unknown model: 'yolov8x_1' is not found
[ERROR] Video25 - video_process.py:L360 - 감지 루프 오류: [StatusCode.NOT_FOUND] Request for unknown model: 'yolov8x_1' is not found
Ultralytics 8.3.149 🚀 Python-3.12.3 torch-2.7.0+cu128 CUDA:0 (NVIDIA RTX 6000 Ada Generation, 48497MiB)
Ultralytics 8.3.149 🚀 Python-3.12.3 torch-2.7.0+cu128 CUDA:0 (NVIDIA RTX 6000 Ada Generation, 48497MiB)
WARNING ⚠️ GitHub assets check failure for https://api.github.com/repos/ultralytics/assets/releases/tags/v8.3.0: 403 rate limit exceeded
WARNING ⚠️ GitHub assets check failure for https://api.github.com/repos/ultralytics/assets/releases/tags/v8.3.0: 403 rate limit exceeded
```

=============================
## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin http://192.168.88.10:30000/skysys/rist-ai-cctv-2025-2nd.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](http://192.168.88.10:30000/skysys/rist-ai-cctv-2025-2nd/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
