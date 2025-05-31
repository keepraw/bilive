# Copyright (c) 2024 bilive.

import os
import time
from pathlib import Path
from src.config import VIDEOS_DIR, MODEL_TYPE
from src.burn.video_processor import render_video, render_then_merge
from src.log.logger import scan_log


def process_folder_merge(folder_path):
    """处理文件夹中的视频文件，合并同一天的视频片段
    Args:
        folder_path: str, 视频文件夹路径
    """
    # 不处理正在录制的文件夹
    flv_files = list(Path(folder_path).glob("*.flv"))
    if flv_files:
        scan_log.info(f"Found flv files in {folder_path}. Skipping.")
        return

    files_by_date = {}

    # 处理录制的文件
    mp4_files = [
        mp4_file
        for mp4_file in Path(folder_path).glob("*.mp4")
        if not mp4_file.name.endswith("-.mp4")
    ]
    for mp4_file in mp4_files:
        date_part = mp4_file.stem.split("_")[1].split("-")[0]

        if date_part not in files_by_date:
            files_by_date[date_part] = []
        files_by_date[date_part].append(mp4_file)

    for date, files in files_by_date.items():
        if len(files) > 1:
            # 如果有多个同一天的片段，合并它们
            sorted_files = sorted(files, key=lambda x: x.stem.split("_")[1])
            scan_log.info(f"Merging {sorted_files}...")
            render_then_merge(sorted_files)
        else:
            for file in files:
                scan_log.info(f"Begin processing {file}...")
                render_video(file)


def process_folder_append(folder_path):
    """按顺序处理文件夹中的视频文件
    Args:
        folder_path: str, 视频文件夹路径
    """
    # 处理录制的文件
    mp4_files = [
        mp4_file
        for mp4_file in Path(folder_path).glob("*.mp4")
        if not mp4_file.name.endswith("-.mp4")
    ]
    mp4_files.sort()
    for file in mp4_files:
        scan_log.info(f"Begin processing {file}...")
        render_video(file)


def process_folder(folder_path):
    """根据配置的模式处理文件夹
    Args:
        folder_path: str, 视频文件夹路径
    """
    if MODEL_TYPE == "merge":
        process_folder_merge(folder_path)
    elif MODEL_TYPE == "append":
        process_folder_append(folder_path)
    else:
        scan_log.error(f"Unknown model type: {MODEL_TYPE}, using append mode as fallback")
        process_folder_append(folder_path)


if __name__ == "__main__":
    room_folder_path = VIDEOS_DIR
    scan_log.info(f"Starting video processing in {MODEL_TYPE} mode")
    
    while True:
        try:
            for room_folder in Path(room_folder_path).iterdir():
                if room_folder.is_dir():
                    process_folder(room_folder)
            scan_log.info("There is no file recorded. Check again in 120 seconds.")
            time.sleep(120)
        except Exception as e:
            scan_log.error(f"Error occurred during processing: {e}")
            time.sleep(120)  # 发生错误时也等待120秒后重试
