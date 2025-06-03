# Copyright (c) 2024 bilive.

import os
import subprocess
from pathlib import Path
from src.log.logger import scan_log
from src.config import RESERVE_FOR_FIXING
from db.conn import insert_upload_queue


def normalize_video_path(filepath):
    """规范化视频路径
    Args:
        filepath: str or Path, 视频路径
    Returns:
        str: 规范化后的路径
    """
    if isinstance(filepath, Path):
        filepath = str(filepath)
    
    parts = filepath.rsplit("/", 1)[-1].split("_")
    date_time_parts = parts[1].split("-")
    new_date_time = f"{date_time_parts[0][:4]}-{date_time_parts[0][4:6]}-{date_time_parts[0][6:8]}-{date_time_parts[1]}-{date_time_parts[2]}"
    return filepath.rsplit("/", 1)[0] + "/" + parts[0] + "_" + new_date_time + "-.mp4"


def format_video(in_video_path, out_video_path):
    """将视频转换为mp4格式
    Args:
        in_video_path: str or Path, 输入视频路径
        out_video_path: str or Path, 输出视频路径
    """
    if isinstance(in_video_path, Path):
        in_video_path = str(in_video_path)
    if isinstance(out_video_path, Path):
        out_video_path = str(out_video_path)

    scan_log.info("Converting video format...")
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
    """处理单个视频文件
    Args:
        video_path: str or Path, 要处理的视频路径
    """
    if isinstance(video_path, Path):
        video_path = str(video_path)

    if not os.path.exists(video_path):
        scan_log.error(f"Video file not found: {video_path}")
        return

    # 获取视频信息
    original_video_path = video_path
    format_video_path = normalize_video_path(original_video_path)

    # 检查文件是否已经是mp4格式
    if original_video_path.lower().endswith('.mp4'):
        scan_log.info("File is already in mp4 format, just renaming...")
        if original_video_path != format_video_path:
            os.rename(original_video_path, format_video_path)
    else:
        # 将flv格式转换为mp4
        format_video(original_video_path, format_video_path)

    # 删除原始文件
    if os.path.exists(original_video_path) and original_video_path != format_video_path:
        os.remove(original_video_path)

    if not insert_upload_queue(format_video_path):
        scan_log.error("Cannot insert the video to the upload queue")


def render_then_merge(video_files):
    """合并多个视频文件
    Args:
        video_files: list, 要合并的视频文件列表
    """
    if not video_files:
        return

    # 创建临时文件列表
    temp_list_path = str(video_files[0].parent / "temp_list.txt")
    with open(temp_list_path, "w", encoding="utf-8") as f:
        for video_file in video_files:
            f.write(f"file '{video_file}'\n")

    # 生成输出文件路径
    output_path = str(video_files[0].parent / f"{video_files[0].stem.split('_')[0]}_merged.mp4")

    # 合并视频
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        temp_list_path,
        "-c",
        "copy",
        output_path,
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")

        # 删除原始文件
        for video_file in video_files:
            if os.path.exists(video_file):
                os.remove(video_file)

        # 删除临时文件
        if os.path.exists(temp_list_path):
            os.remove(temp_list_path)

        # 添加到上传队列
        if not insert_upload_queue(output_path):
            scan_log.error("Cannot insert the merged video to the upload queue")

    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error merging videos: {e.stderr}")
        if not RESERVE_FOR_FIXING:
            # 如果不需要保留文件用于修复，则删除所有相关文件
            for video_file in video_files:
                if os.path.exists(video_file):
                    os.remove(video_file)
            if os.path.exists(temp_list_path):
                os.remove(temp_list_path)
        raise 