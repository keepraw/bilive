# Copyright (c) 2024 bilive.

import queue
import time
from src.burn.render_video import render_video
from src.log.logger import scan_log


class VideoRenderQueue:
    def __init__(self):
        self.render_queue = queue.Queue()

    def pipeline_render(self, video_path):
        """Add video to render queue
        Args:
            video_path: str, the path of video to be processed
        """
        self.render_queue.put(video_path)

    def monitor_queue(self):
        """Monitor the render queue and process videos"""
        while True:
            if not self.render_queue.empty():
                video_path = self.render_queue.get()
                try:
                    render_video(video_path)
                except Exception as e:
                    scan_log.error(f"Error processing video {video_path}: {e}")
            else:
                time.sleep(1)
