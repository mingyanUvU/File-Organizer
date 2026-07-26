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

    if input_yes_no(f"{t('是否打开文件所在文件夹？')}(y/n): "):
        open_folder(os.path.dirname(file_path))

    ext = os.path.splitext(file_path)[1].lower()
    ext_mappings = cfg["extensions"].get(ext, [])

    target = None

    if len(ext_mappings) == 0:
        print(f"{t('未识别的后缀')}{ext}，{t('请从所有分类中选择')}")
        target = select_classification(cfg, t("请从所有分类中选择"))
        if target is None:
            return

    elif len(ext_mappings) == 1:
        g, c = ext_mappings[0]
        cat_path = cfg["groups"].get(g, {}).get(c, "")
        label = f"{g} {t('→')} {c}"
        print(f"{t('建议分类：')}{label}  ({cat_path})")
        if input_yes_no(f"{t('是否使用此分类？')}(y/n): "):
            target = (g, c)
        else:
            target = select_classification(cfg, t("请重新选择分类"))
            if target is None:
                return

    else:
        print(f"{ext}{t('有')}{len(ext_mappings)}{t('个指向')}")
        for i, (g, c) in enumerate(ext_mappings, 1):
            cat_path = cfg["groups"].get(g, {}).get(c, "")
            print(f"  [{i}] {g} {t('→')} {c}  ({cat_path})")
        print(t("  [0] 从所有分类中选择"))
        m_valid = {str(i) for i in range(1, len(ext_mappings) + 1)} | {"0"}
        m_choice = input_option(t("输入编号: "), m_valid)
        if m_choice == "0":
            target = select_classification(cfg, t("从所有分类中选择"))
            if target is None:
                return
        else:
            target = ext_mappings[int(m_choice) - 1]

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

    default_name = sanitize_folder_name(os.path.splitext(os.path.basename(file_path))[0])
    folder_input = input(f"{t('文件夹名（直接回车默认：')}{default_name}{t('）: ')}").strip()
    folder_name = sanitize_folder_name(folder_input) if folder_input else default_name
    if not folder_name:
        folder_name = default_name

    target_dir = os.path.join(cat_path, folder_name)

    try:
        os.makedirs(target_dir, exist_ok=True)
        dst = os.path.join(target_dir, os.path.basename(file_path))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(file_path, target_dir)
        print(f"\n{t('已移动到：')}{group_name} {t('→')} {cat_name} {t('→')} {folder_name}")
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
    target = select_classification(cfg, t("请从所有分类中选择"))
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

    default_name = sanitize_folder_name(os.path.basename(folder_path))
    folder_input = input(f"{t('文件夹名（直接回车默认：')}{default_name}{t('）: ')}").strip()
    folder_name = sanitize_folder_name(folder_input) if folder_input else default_name

    target_dir = os.path.join(cat_path, folder_name)

    try:
        os.makedirs(target_dir, exist_ok=True)
        dst = os.path.join(target_dir, os.path.basename(folder_path))
        if os.path.exists(dst):
            print(t("目标位置已存在同名项。"))
            return
        shutil.move(folder_path, target_dir)
        print(f"\n{t('已移动到：')}{group_name} {t('→')} {cat_name} {t('→')} {folder_name}")
    except Exception as e:
        print(f"{t('移动失败：')}{e}")
        return

    if input_yes_no(f"{t('是否打开目标文件夹？')}(y/n): "):
        open_folder(target_dir)
