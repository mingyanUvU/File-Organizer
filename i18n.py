import json
import os


# ========== 国际化 ==========

_current_lang = "zh"
_T = {}


def _load_T():
    global _T
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_translations.json")
    with open(path, encoding="utf-8") as f:
        _T = json.load(f)


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
