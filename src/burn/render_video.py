# Copyright (c) 2024 bilive.

import argparse
import os
import subprocess
from src.config import (
    SRC_DIR,
    MODEL_TYPE,
    VIDEOS_DIR,
)
from src.log.logger import scan_log
from db.conn import insert_upload_queue
from src.upload.extract_video_info import get_video_info


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
    xml_path = original_video_path[:-4] + ".xml"
    ass_path = original_video_path[:-4] + ".ass"
    srt_path = original_video_path[:-4] + ".srt"
    jsonl_path = original_video_path[:-4] + ".jsonl"

    # Delete relative files
    for remove_path in [original_video_path, xml_path, ass_path, srt_path, jsonl_path]:
        if os.path.exists(remove_path):
            os.remove(remove_path)

    if not insert_upload_queue(format_video_path):
        scan_log.error("Cannot insert the video to the upload queue")
