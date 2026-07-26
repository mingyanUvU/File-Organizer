import os
import sys
import json


# ========== 路径 ==========

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_PATH = os.path.join(BASE_DIR, "分类配置.json")


# ========== 默认配置 ==========

DEFAULT_CONFIG = {
    "version": 1,
    "settings": {
        "source_directories": ["D:\\Downloads"],
        "language": "zh"
    },
    "groups": {
        "AI Draw": {
            "绘画模型": r"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\models\Stable-diffusion",
            "Lora":      r"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\models\Lora",
            "VAE":       r"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\models\VAE",
            "Embedding": r"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\embeddings"
        },
        "默认分类": {}
    },
    "extensions": {
        ".safetensors": [["AI Draw", "绘画模型"]],
        ".ckpt":        [["AI Draw", "绘画模型"]],
        ".pt":          [["AI Draw", "VAE"]],
        ".png":         [["默认分类", "图片"]],
        ".jpg":         [["默认分类", "图片"]],
        ".jpeg":        [["默认分类", "图片"]],
        ".webp":        [["默认分类", "图片"]],
        ".pdf":         [["默认分类", "文档"]],
        ".docx":        [["默认分类", "文档"]],
        ".xlsx":        [["默认分类", "文档"]],
        ".txt":         [["默认分类", "文档"]],
        ".zip":         [["默认分类", "压缩包"]],
        ".rar":         [["默认分类", "压缩包"]],
        ".7z":          [["默认分类", "压缩包"]]
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
        config["settings"] = {"source_directories": ["D:\\Downloads"], "language": "zh"}
    return config


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
