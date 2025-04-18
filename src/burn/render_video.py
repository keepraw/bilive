# Copyright (c) 2024 bilive.

import argparse
import os
import subprocess
from src.config import (
    SRC_DIR,
    MODEL_TYPE,
    AUTO_SLICE,
    SLICE_DURATION,
    MIN_VIDEO_SIZE,
    VIDEOS_DIR,
    SLICE_NUM,
    SLICE_OVERLAP,
    SLICE_STEP,
)
from src.danmaku.generate_danmakus import get_resolution, process_danmakus
from src.subtitle.subtitle_generator import generate_subtitle
from src.burn.render_command import render_command
from autoslice import slice_video_by_danmaku
from src.autoslice.inject_metadata import inject_metadata
from src.autoslice.title_generator import generate_title
from src.upload.extract_video_info import get_video_info
from src.log.logger import scan_log
from db.conn import insert_upload_queue


def normalize_video_path(filepath):
    """Normalize the video path to upload
    Args:
        filepath: str, the path of video
    """
    parts = filepath.rsplit("/", 1)[-1].split("_")
    date_time_parts = parts[1].split("-")
    new_date_time = f"{date_time_parts[0][:4]}-{date_time_parts[0][4:6]}-{date_time_parts[0][6:8]}-{date_time_parts[1]}-{date_time_parts[2]}"
    return filepath.rsplit("/", 1)[0] + "/" + parts[0] + "_" + new_date_time + "-.mp4"


def check_file_size(file_path):
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    return file_size_mb


def render_video(video_path):
    if not os.path.exists(video_path):
        scan_log.error(f"File {video_path} does not exist.")
        return

    original_video_path = str(video_path)
    format_video_path = normalize_video_path(original_video_path)
    
    # 直接重命名文件
    try:
        os.rename(original_video_path, format_video_path)
        scan_log.info("Video file renamed successfully!")
    except Exception as e:
        scan_log.error(f"Error in renaming video: {e}")
        return

    # 加入上传队列
    if not insert_upload_queue(format_video_path):
        scan_log.error("Cannot insert the video to the upload queue")
