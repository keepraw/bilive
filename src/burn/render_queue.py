# Copyright (c) 2024 bilive.

import queue
import time
from src.burn.render_video import process_video
from src.log.logger import scan_log


class VideoRenderQueue:
    def __init__(self):
        self.render_queue = queue.Queue()

    def pipeline_render(self, video_path):
        self.render_queue.put(video_path)

    def monitor_queue(self):
        while True:
            if not self.render_queue.empty():
                video_path = self.render_queue.get()
                try:
                    process_video(video_path)
                except Exception as e:
                    scan_log.error(f"Error processing video {video_path}: {e}")
            else:
                time.sleep(1)
