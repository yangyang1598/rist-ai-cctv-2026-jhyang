#!/bin/bash
set -e
echo "Running App..."
cd /home/rist/rist-ai-cctv-2025-2nd
echo "Current Directory is: $(pwd)"
uv run /home/rist/rist-ai-cctv-2025-2nd/main_window.py
echo "App execution completed successfully" 
