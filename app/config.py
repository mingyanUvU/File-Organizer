import os
import sys
import json


# ========== 路径 ==========

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


# ========== 默认配置 ==========

DEFAULT_CONFIG = {
    "version": 1,
    "settings": {"source_directories": [], "language": "zh"},
    "groups": {
        "Windows\u7cfb\u7edf\u9ed8\u8ba4": {
            "\u6587\u6863": os.path.join(os.path.expanduser("~"), "Documents"),
            "\u56fe\u7247": os.path.join(os.path.expanduser("~"), "Pictures"),
            "\u89c6\u9891": os.path.join(os.path.expanduser("~"), "Videos"),
            "\u97f3\u4e50": os.path.join(os.path.expanduser("~"), "Music"),
        }
    },
    "extensions": {
        ".pdf": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u6587\u6863"]],
        ".docx": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u6587\u6863"]],
        ".txt": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u6587\u6863"]],
        ".md": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u6587\u6863"]],
        ".xlsx": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u6587\u6863"]],
        ".csv": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u6587\u6863"]],
        ".png": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u56fe\u7247"]],
        ".jpg": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u56fe\u7247"]],
        ".jpeg": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u56fe\u7247"]],
        ".gif": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u56fe\u7247"]],
        ".bmp": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u56fe\u7247"]],
        ".webp": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u56fe\u7247"]],
        ".mp4": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u89c6\u9891"]],
        ".avi": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u89c6\u9891"]],
        ".mkv": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u89c6\u9891"]],
        ".mp3": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u97f3\u4e50"]],
        ".wav": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u97f3\u4e50"]],
        ".flac": [["Windows\u7cfb\u7edf\u9ed8\u8ba4", "\u97f3\u4e50"]],
    }
}


# ========== 读写 ==========

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        config = dict(DEFAULT_CONFIG)
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    if "settings" not in config:
        config["settings"] = {"source_directories": [], "language": "zh"}
    return config


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
