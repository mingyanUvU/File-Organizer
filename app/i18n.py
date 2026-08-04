import json
import os
import sys


# ========== 国际化 ==========

_current_lang = "zh"
_T = {}


def _load_T():
    global _T
    path = _resource_path("_translations.json")
    with open(path, encoding="utf-8") as f:
        _T = json.load(f)


def _resource_path(name):
    """打包后从 PyInstaller 解压目录读取数据文件，开发模式读取源码目录"""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        candidates = [
            os.path.join(base, name),
            os.path.join(base, "app", name),
            os.path.join(os.path.dirname(sys.executable), name),
        ]
        for p in candidates:
            if os.path.exists(p):
                return p
        return candidates[0]
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)


_load_T()


def t(key: str) -> str:
    """按当前语言取翻译文本"""
    val = _T.get(key)
    if val:
        return val[0] if _current_lang == "zh" else val[1]
    return key


def set_language(lang: str):
    """设置当前语言（zh / en）"""
    global _current_lang
    _current_lang = lang
