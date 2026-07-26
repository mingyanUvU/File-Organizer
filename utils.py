import os
import re
from datetime import datetime
from i18n import t
from config import save_config


# ========== 通用 ==========

def sanitize_folder_name(name: str) -> str:
    invalid = R'\ / : * ? " < > |'
    for ch in invalid:
        name = name.replace(ch, "_")
    return name.strip(" .")


def input_yes_no(prompt: str) -> bool:
    while True:
        val = input(prompt).strip().lower()
        if val in ("y", "yes", "是"):
            return True
        if val in ("n", "no", "否"):
            return False
        print(t("输入无效，请输入 y/n"))


def input_option(prompt: str, valid_options: set) -> str:
    while True:
        val = input(prompt).strip().lower()
        if val in valid_options:
            return val
        print(t("输入无效"))


def open_folder(path: str):
    if os.path.isdir(path):
        os.startfile(path)
    else:
        print(f"{t('路径不存在：')}{path}")


EXCLUDED_FILES = {"desktop.ini", "thumbs.db", ".ds_store"}
# 临时文件/未完成下载，跳过
EXCLUDED_EXTS = {".tmp", ".temp", ".crdownload", ".download", ".part"}


def get_latest_file(folder: str) -> str | None:
    """只扫当前目录；文件夹用 mtime（文件变化时更新），文件用 ctime"""
    if not os.path.isdir(folder):
        print(f"{t('错误：目录不存在 — ')}{folder}")
        return None

    entries = []
    for item in os.listdir(folder):
        full = os.path.join(folder, item)
        if item.lower() in EXCLUDED_FILES or item.startswith("~$"):
            continue
        if os.path.isfile(full) and os.path.splitext(item)[1].lower() in EXCLUDED_EXTS:
            continue
        entries.append(full)

    if not entries:
        print(t("目录为空，没有可处理的文件。"))
        return None

    def _time(p):
        return os.path.getmtime(p) if os.path.isdir(p) else os.path.getctime(p)

    return max(entries, key=_time)
def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def show_file_info(file_path: str):
    stat = os.stat(file_path)
    ctime = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{t('  文件名：')}{os.path.basename(file_path)}")
    print(f"{t('  位置：')}{os.path.dirname(file_path)}")
    print(f"{t('  后缀名：')}{os.path.splitext(file_path)[1].lower()}")
    print(f"{t('  大小：')}{format_size(stat.st_size)}")
    print(f"{t('  加入时间：')}{ctime}")


# ========== 分类选择（菜单组件，被 organize / extensions 共用） ==========

def select_classification(cfg: dict, prompt: str = "请选择分类") -> tuple | None:
    """返回 (group_name, category_name) 或 None"""
    groups = cfg["groups"]

    # 选分组
    group_list = list(groups.keys())
    print(f"\n--- {prompt} ---")
    print(t("选择分组："))
    for i, g in enumerate(group_list, 1):
        print(f"  [{i}] {g}")
    print(t("  [a] 新增分组"))
    g_valid = {str(i) for i in range(1, len(group_list) + 1)} | {"a", "0"}
    g_choice = input_option(t("输入编号 (0 取消): "), g_valid)
    if g_choice == "0":
        return None
    if g_choice == "a":
        name = input(t("新分组名 (0 取消): ")).strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        if name in groups:
            print(t("该分组已存在。"))
            return None
        groups[name] = {}
        save_config(cfg)
        print(f"{t('✓ 已创建分组：')}{name}")
        group_name = name
    else:
        group_name = group_list[int(g_choice) - 1]

    # 选分类
    cat_dict = groups[group_name]
    cat_list = list(cat_dict.keys())

    if not cat_list:
        print(f'{t("分组")}{group_name}{t("下没有分类，请先新增。")}')
        name = input(t("新分类名 (0 取消): ")).strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        path_input = input(t("目标路径（可选，留空后续设置）: ")).strip()
        cat_dict[name] = path_input
        save_config(cfg)
        print(f"{t('✓ 已创建分类：')}{group_name} → {name}")
        return group_name, name

    print(f"{group_name}{t(' 下的分类：')}")
    for i, c in enumerate(cat_list, 1):
        path_hint = cat_dict[c] if cat_dict[c] else t("（未设置）")
        print(f"  [{i}] {c}  {t('→')}  {path_hint}")
    print(t("  [a] 新增分类"))
    c_valid = {str(i) for i in range(1, len(cat_list) + 1)} | {"a", "0"}
    c_choice = input_option(t("输入编号 (0 返回): "), c_valid)
    if c_choice == "0":
        return None
    if c_choice == "a":
        name = input(t("新分类名 (0 取消): ")).strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        if name in cat_dict:
            print(t("该分类已存在。"))
            return None
        path_input = input(t("目标路径（可选，留空后续设置）: ")).strip()
        cat_dict[name] = path_input
        save_config(cfg)
        print(f"{t('✓ 已创建分类：')}{group_name} → {name}")
        return group_name, name

    cat_name = cat_list[int(c_choice) - 1]
    return group_name, cat_name
