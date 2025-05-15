# Copyright (c) 2024 bilive.

import os
import subprocess
from src.log.logger import scan_log


def render_command(
    in_video_path, out_video_path
):
    """Burn the danmakus into the videos
    Args:
        in_video_path: str, the path of video
        out_video_path: str, the path of rendered video
    """
    in_ass_path = in_video_path[:-4] + ".ass"
    if not os.path.isfile(in_ass_path):
        scan_log.warning("Cannot find danmaku file, return directly")
        subprocess.run(
            ["mv", in_video_path, out_video_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return

    scan_log.info("Current Mode: CPU")
    cpu_ass_command = [
        "ffmpeg",
        "-y",
        "-i",
        in_video_path,
        "-vf",
        f"ass={in_ass_path}",
        "-preset",
        "ultrafast",
        out_video_path,
    ]
    try:
        result = subprocess.run(
            cpu_ass_command, check=True, capture_output=True, text=True
        )
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")
