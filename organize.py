import os
import shutil
from config import save_config
from i18n import t
from utils import (
    sanitize_folder_name, input_yes_no, input_option,
    open_folder, show_file_info, select_classification
)


# ========== 整理文件 ==========

def organize_file(file_path: str, cfg: dict):
    if not os.path.isfile(file_path):
        print(t("文件不存在。"))
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
