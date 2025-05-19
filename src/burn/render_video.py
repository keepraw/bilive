# Copyright (c) 2024 bilive.

import os
import subprocess
import json
from src.config import (
    SRC_DIR,
    MODEL_TYPE,
    VIDEOS_DIR,
    TID,
)
from src.log.logger import scan_log
from db.conn import insert_upload_queue
from src.upload.extract_video_info import get_video_info
from src.upload.generate_upload_data import generate_video_data


def normalize_video_path(filepath):
    """Normalize the video path to upload
    Args:
        filepath: str, the path of video
    """
    parts = filepath.rsplit("/", 1)[-1].split("_")
    date_time_parts = parts[1].split("-")
    new_date_time = f"{date_time_parts[0][:4]}-{date_time_parts[0][4:6]}-{date_time_parts[0][6:8]}-{date_time_parts[1]}-{date_time_parts[2]}"
    return filepath.rsplit("/", 1)[0] + "/" + parts[0] + "_" + new_date_time + "-.mp4"


def cleanup_files(video_path):
    """Clean up related files (xml, ass, srt, jsonl)
    Args:
        video_path: str, the path of video file
    """
    base_path = video_path[:-4]  # 移除 .mp4 后缀
    for ext in [".xml", ".ass", ".srt", ".jsonl"]:
        file_path = base_path + ext
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                scan_log.debug(f"Removed {file_path}")
            except Exception as e:
                scan_log.error(f"Failed to remove {file_path}: {e}")


def get_video_metadata(video_path):
    """Get all necessary metadata for video upload
    Args:
        video_path: str, the path of video file
    Returns:
        dict: metadata dictionary containing all necessary fields
    """
    # 获取基本视频信息
    title, artist, date = get_video_info(video_path)
    if title is None:
        return None

    # 获取上传所需的所有元数据
    title, desc, tid, tag, source, cover, dynamic = generate_video_data(video_path)

    # 构建元数据字典
    metadata = {
        "title": title,
        "artist": artist,
        "date": date,
        "description": desc,
        "tid": str(tid),
        "tag": tag,
        "source": source,
        "dynamic": dynamic
    }
    return metadata


def merge_videos(video_paths, output_path, metadata=None):
    """Merge multiple video files into one and preserve metadata
    Args:
        video_paths: list, paths of video files to merge
        output_path: str, path of output video file
        metadata: dict, metadata dictionary containing all necessary fields
    Returns:
        bool: True if merge successful, False otherwise
    """
    try:
        # 创建临时文件列表
        temp_list = output_path + ".txt"
        with open(temp_list, "w", encoding="utf-8") as f:
            for video in video_paths:
                f.write(f"file '{video}'\n")

        # 使用 ffmpeg 合并视频，保留元数据
        command = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", temp_list,
        ]
        
        # 如果有元数据，添加到命令中
        if metadata:
            for key, value in metadata.items():
                if value:  # 只添加非空的元数据
                    command.extend(["-metadata", f"{key}={value}"])
        
        command.extend([
            "-c", "copy",
            output_path
        ])
        
        subprocess.run(command, check=True, capture_output=True)
        os.remove(temp_list)
        return True
    except Exception as e:
        scan_log.error(f"Error merging videos: {e}")
        if os.path.exists(temp_list):
            os.remove(temp_list)
        return False


def process_video(video_path):
    """Process video file and add to upload queue
    Args:
        video_path: str, the path of video file
    """
    if not os.path.exists(video_path):
        scan_log.error(f"File {video_path} does not exist.")
        return

    # 获取视频元数据
    metadata = get_video_metadata(video_path)
    if metadata is None:
        scan_log.error("Failed to get video metadata")
        return

    # 清理相关文件
    cleanup_files(video_path)

    # 如果是 append 模式，直接重命名并加入上传队列
    if MODEL_TYPE == "append":
        format_video_path = normalize_video_path(video_path)
        os.rename(video_path, format_video_path)
        if not insert_upload_queue(format_video_path):
            scan_log.error("Cannot insert the video to the upload queue")
        return

    # 如果是 merge 模式，需要合并视频
    if MODEL_TYPE == "merge":
        # 获取同一天的所有视频文件
        video_dir = os.path.dirname(video_path)
        video_name = os.path.basename(video_path)
        date_str = video_name.split("_")[1].split("-")[0]
        video_files = []
        for file in os.listdir(video_dir):
            if file.endswith(".mp4") and date_str in file:
                video_files.append(os.path.join(video_dir, file))
                # 清理每个视频的相关文件
                cleanup_files(os.path.join(video_dir, file))
        
        if len(video_files) > 1:
            # 按文件名排序
            video_files.sort()
            output_path = normalize_video_path(video_files[0])
            if merge_videos(video_files, output_path, metadata):
                # 删除原始文件
                for file in video_files:
                    if file != output_path:
                        os.remove(file)
                if not insert_upload_queue(output_path):
                    scan_log.error("Cannot insert the merged video to the upload queue")
            else:
                scan_log.error("Failed to merge videos")
        else:
            # 只有一个视频文件，直接处理
            format_video_path = normalize_video_path(video_path)
            os.rename(video_path, format_video_path)
            if not insert_upload_queue(format_video_path):
                scan_log.error("Cannot insert the video to the upload queue")
        return

    # 如果是 pipeline 模式，直接加入上传队列
    if MODEL_TYPE == "pipeline":
        if not insert_upload_queue(video_path):
            scan_log.error("Cannot insert the video to the upload queue")
        return
