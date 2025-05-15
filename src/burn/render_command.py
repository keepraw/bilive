# Copyright (c) 2024 bilive.

import os
import subprocess
from src.log.logger import scan_log


def render_command(in_video_path, out_video_path):
    """Process the video file
    Args:
        in_video_path: str, the path of video
        out_video_path: str, the path of output video
    """
    scan_log.info("Processing video...")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        in_video_path,
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        out_video_path,
    ]
    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True
        )
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")
        # 如果处理失败，直接复制原文件
        subprocess.run(
            ["mv", in_video_path, out_video_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
