import os
import sys
import json


# ========== 路径 ==========

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "分类配置.json")


# ========== 默认配置 ==========

DEFAULT_CONFIG = {
    "version": 1,
    "settings": {"source_directories": [], "language": "zh"},
    "groups": {},
    "extensions": {}
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
