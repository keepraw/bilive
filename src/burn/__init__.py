# Copyright (c) 2024 bilive.

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.burn.video_processor import render_video, render_then_merge

__all__ = ["render_video", "render_then_merge"]
