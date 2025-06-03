# Copyright (c) 2024 bilive.

import os
from pathlib import Path
from datetime import datetime
import configparser
import toml
from db.conn import create_table


def load_config_from_toml(file_path):
    """
    load config from toml file and update global variables
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = toml.load(file)
            return config
    except FileNotFoundError:
        print(f"cannot find {file_path}", flush=True)
    except toml.TomlDecodeError as e:
        print(f"cannot parse {file_path} as a valid toml file, error: {e}", flush=True)
    except Exception as e:
        print(f"unknown error when loading config file, error: {e}", flush=True)
    return None


SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
BILIVE_DIR = str(Path(SRC_DIR).parent)
LOG_DIR = os.path.join(BILIVE_DIR, "logs")
VIDEOS_DIR = os.path.join(BILIVE_DIR, "Videos")
if not os.path.exists(SRC_DIR + "/db/data.db"):
    print("Initialize the database", flush=True)
    create_table()

config = load_config_from_toml(os.path.join(BILIVE_DIR, "bilive.toml"))
if config is None:
    print("failed to load config file, please check twice", flush=True)
    exit(1)

MODEL_TYPE = config.get("model", {}).get("model_type")

TITLE = config.get("video", {}).get("title")
DESC = config.get("video", {}).get("description")
TID = config.get("video", {}).get("tid")
GIFT_PRICE_FILTER = config.get("video", {}).get("gift_price_filter")
RESERVE_FOR_FIXING = config.get("video", {}).get("reserve_for_fixing")
UPLOAD_LINE = config.get("video", {}).get("upload_line")
