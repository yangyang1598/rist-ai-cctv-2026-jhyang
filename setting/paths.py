from pathlib import Path


HOME_DIR = Path.home()
PROJECT_ROOT = HOME_DIR / "rist-ai-cctv-2025-2nd"
CONFIG_DIR = PROJECT_ROOT / "config"
GLOBAL_SETTING_PATH = CONFIG_DIR / "global_setting.ini"
VIDEO_OUTPUT_DIR = PROJECT_ROOT / "video"
IMAGE_OUTPUT_DIR = PROJECT_ROOT / "image"
TRACKER_LOCATION = PROJECT_ROOT / "widget/video_process_pipeline/bytetrack.yaml"