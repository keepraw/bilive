# Copyright (c) 2024 bilive.

import os
import time
import codecs
from datetime import datetime
from src.upload.extract_video_info import (
    generate_title,
    generate_desc,
    generate_tag,
    generate_source,
)
import subprocess
import json
from src.config import TID


def generate_video_data(video_path):
    title = generate_title(video_path)
    desc = generate_desc(video_path)
    tid = TID
    tag = generate_tag(video_path)
    source = generate_source(video_path)
    cover = ""  # 默认不设置封面
    dynamic = ""  # 默认不设置动态
    return title, desc, tid, tag, source, cover, dynamic


if __name__ == "__main__":
    pass
