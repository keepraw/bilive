# Copyright (c) 2024 bilive.

import argparse
import os
import subprocess
from src.log.logger import scan_log
from src.config import (
    MODEL_TYPE,
    VIDEOS_DIR,
    RESERVE_FOR_FIXING,
    GPU_EXIST,
)
from src.upload.upload_queue import insert_upload_queue


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


def format_video(in_video_path, out_video_path):
    """Convert flv video to mp4 format
    Args:
        in_video_path: str, the path of input flv video
        out_video_path: str, the path of output mp4 video
    """
    if GPU_EXIST:
        scan_log.info("Current Mode: GPU")
        command = [
            "ffmpeg",
            "-y",
            "-hwaccel",
            "cuda",
            "-c:v",
            "h264_cuvid",
            "-i",
            in_video_path,
            "-c:v",
            "h264_nvenc",
            "-preset",
            "p4",
            "-tune",
            "hq",
            "-b:v",
            "0",
            "-maxrate",
            "5M",
            "-bufsize",
            "10M",
            out_video_path,
        ]
    else:
        scan_log.info("Current Mode: CPU")
        command = [
            "ffmpeg",
            "-y",
            "-i",
            in_video_path,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            out_video_path,
        ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")
        raise


def render_video(video_path):
    if not os.path.exists(video_path):
        scan_log.error(f"Video file not found: {video_path}")
        return

    # Get the video info
    original_video_path = video_path
    format_video_path = normalize_video_path(original_video_path)
    xml_path = original_video_path[:-4] + ".xml"
    jsonl_path = original_video_path[:-4] + ".jsonl"

    # Format the video from flv to mp4
    format_video(original_video_path, format_video_path)

    # Delete relative files
    for remove_path in [original_video_path, xml_path, jsonl_path]:
        if os.path.exists(remove_path):
            os.remove(remove_path)

    if not insert_upload_queue(format_video_path):
        scan_log.error("Cannot insert the video to the upload queue")
