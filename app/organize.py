import os
import shutil
from datetime import datetime
from config import save_config
from i18n import t
from utils import (
    sanitize_folder_name, input_yes_no, input_option,
    open_folder, show_file_info, select_classification, get_latest_file
)


# ========== 整理文件 ==========

def organize_file(file_path: str, cfg: dict):
    if not os.path.exists(file_path):
        print(t("路径不存在。"))
        return

    if os.path.isdir(file_path):
        _handle_folder(file_path, cfg)
        return

    print("\n" + "=" * 48)
    show_file_info(file_path)
    print("=" * 48)

    print("=" * 48)

    ext = os.path.splitext(file_path)[1].lower()
    ext_mappings = cfg["extensions"].get(ext, [])

    while True:
        # Combined menu
        print(f"\n" + t("操作选项："))
        print("  [1] " + t("打开所在文件夹"))
        idx = 2
        for g, c in ext_mappings:
            label = f"  [{idx}] {g} \u2192 {c}"
            if idx == 2 and len(ext_mappings) == 1:
                label = f"  [{idx}] " + t("使用默认分类") + f" \u2192 {g} \u2192 {c}"
            print(label)
            idx += 1
        manual_idx = idx
        print(f"  [{manual_idx}] " + t("选择其他分类"))
        idx += 1
        pi = idx
        print(f"  [{pi}] " + t("直接输入路径"))
        idx += 1
        print("  [0] " + t("取消"))

        valid = {"0", "1", str(pi), str(manual_idx)}
        if ext_mappings:
            valid |= {str(i) for i in range(2, 2 + len(ext_mappings))}
        choice = input_option(t("输入编号: "), valid)

        if choice == "0":
            return
        if choice == "1":
            open_folder(os.path.dirname(file_path))
            continue
        if choice == str(pi):
            p = input(t("请输入目标路径: ")).strip()
            if not p:
                continue
            if not os.path.isabs(p):
                print(t("请输入绝对路径。"))
                continue
            target_dir = p
            try:
                os.makedirs(target_dir, exist_ok=True)
                dst = os.path.join(target_dir, os.path.basename(file_path))
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.move(file_path, target_dir)
                print(t("已移动到：") + target_dir)
            except Exception as e:
                print(t("移动失败：") + str(e))
                return
            if input_yes_no(t("是否打开目标文件夹？") + "(y/n): "):
                open_folder(target_dir)
            return
        if choice in {str(i) for i in range(2, 2 + len(ext_mappings))}:
            target = ext_mappings[int(choice) - 2]
            break
        target = select_classification(cfg, t("请从所有分类中选择"), require_path=True)
        if target is None:
            continue
        break

    group_name, cat_name = target
    cat_path = cfg["groups"].get(group_name, {}).get(cat_name, "")

    if not cat_path:
        print(f"{t('分类')}{group_name} {t('→')} {cat_name}{t('未设置目标路径。')}")
        if input_yes_no(f"{t('现在设置？')}(y/n): "):
            new_path = input(f"{t('请输入路径')}: ").strip()
            if not os.path.isabs(new_path):
                print(t("路径无效，请使用绝对路径。"))
                return
            cfg["groups"][group_name][cat_name] = new_path
            save_config(cfg)
            cat_path = new_path
        else:
            print(t("取消操作。"))
            return

    # folder name prompt
    folder_input = input(f"  {t('建立文件夹？')} {t('？默认归档，回车直接移入。')}\n  > ").strip()
    if folder_input in (chr(63), chr(65311)):  # ? or ？
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H-%M")
        target_dir = os.path.join(cat_path, date_str, time_str)
    elif folder_input:
        folder_name = sanitize_folder_name(folder_input)
        target_dir = os.path.join(cat_path, folder_name)
    else:
        target_dir = cat_path

    try:
        os.makedirs(target_dir, exist_ok=True)
        dst = os.path.join(target_dir, os.path.basename(file_path))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(file_path, target_dir)
        print(t("已移动到：") + target_dir)
    except Exception as e:
        print(f"{t('移动失败：')}{e}")
        return

    if input_yes_no(f"{t('是否打开目标文件夹？')}(y/n): "):
        open_folder(target_dir)


# ========== 文件夹处理 ==========

def _handle_folder(folder_path: str, cfg: dict):
    """处理文件夹：整体转移或进入内部"""
    items = os.listdir(folder_path)
    sub_files = [f for f in items if os.path.isfile(os.path.join(folder_path, f))]
    sub_dirs = [f for f in items if os.path.isdir(os.path.join(folder_path, f))]

    print("\n" + "=" * 48)
    print(f"  {t('名称：')}{os.path.basename(folder_path)}")
    print(f"  {t('位置：')}{os.path.dirname(folder_path)}")
    print(f"  {t('内容：')}{len(sub_files)}{t('文件，')}{len(sub_dirs)}{t('文件夹')}")
    print(f"  {t('创建时间：')}{datetime.fromtimestamp(os.path.getctime(folder_path)).strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 48)

    print(f"\n{t('这是一个文件夹，如何处理？')}")
    print(f"  [1] {t('整体转移整个文件夹')}")
    print(f"  [2] {t('进入内部查找最新项')}")
    print(f"  [0] {t('取消')}")
    choice = input_option(t("输入编号: "), {"1", "2", "0"})

    if choice == "0":
        return
    elif choice == "2":
        latest = get_latest_file(folder_path)
        if latest:
            organize_file(latest, cfg)
        return

    # 整体转移
    target = select_classification(cfg, t("请从所有分类中选择"), require_path=True)
    if target is None:
        return

    group_name, cat_name = target
    cat_path = cfg["groups"].get(group_name, {}).get(cat_name, "")

    if not cat_path:
        print(f"{group_name} {t('→')} {cat_name}{t('未设置目标路径。')}")
        if input_yes_no(f"{t('现在设置？')}(y/n): "):
            new_path = input(f"{t('请输入路径')}: ").strip()
            if not os.path.isabs(new_path):
                print(t("路径无效，请使用绝对路径。"))
                return
            cfg["groups"][group_name][cat_name] = new_path
            save_config(cfg)
            cat_path = new_path
        else:
            print(t("取消操作。"))
            return

    folder_input = input(f"  {t('建立文件夹？')} {t('？默认归档，回车直接移入。')}\n  > ").strip()
    if folder_input in (chr(63), chr(65311)):
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H-%M")
        target_dir = os.path.join(cat_path, date_str, time_str)
    elif folder_input:
        folder_name = sanitize_folder_name(folder_input)
        target_dir = os.path.join(cat_path, folder_name)
    else:
        target_dir = cat_path

    try:
        os.makedirs(target_dir, exist_ok=True)
        dst = os.path.join(target_dir, os.path.basename(folder_path))
        if os.path.exists(dst):
            print(t("目标位置已存在同名项。"))
            return
        shutil.move(folder_path, target_dir)
        print(t("已移动到：") + target_dir)
    except Exception as e:
        print(f"{t('移动失败：')}{e}")
        return

    if input_yes_no(f"{t('是否打开目标文件夹？')}(y/n): "):
        open_folder(target_dir)
