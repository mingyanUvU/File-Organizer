import sys
import os
import ctypes
from config import load_config, CONFIG_PATH
from i18n import set_language as i18n_set_language, t
from utils import input_option, get_latest_file
from organize import organize_file
from categories import manage_categories
from extensions import manage_extensions
from settings import manage_settings


# ========== 配置管理子菜单 ==========

def manage_config(cfg: dict):
    while True:
        print("\n" + "=" * 48)
        print(t("  配置管理"))
        print("=" * 48)
        print(t("  [1] 管理分类"))
        print(t("  [2] 管理后缀映射"))
        print(t("  [0] 返回主菜单"))
        choice = input_option(t("输入编号: "), {"1", "2", "0"})
        if choice == "0":
            return
        if choice == "1":
            manage_categories(cfg)
        elif choice == "2":
            manage_extensions(cfg)


# ========== 主菜单 ==========

def main():
    # 控制台 UTF-8
    if sys.platform == "win32":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)

    cfg = load_config()
    i18n_set_language(cfg.get("settings", {}).get("language", "zh"))

    while True:
        print("\n" + "=" * 48)
        print("  File Organizer")
        print("=" * 48)
        print(t("  [1] 整理最新下载文件"))
        print(t("  [2] 移动指定文件"))
        print(t("  [3] 管理分类配置"))
        print(t("  [4] 设置"))
        print(t("  [0] 退出"))
        choice = input_option(t("输入编号: "), {"1", "2", "3", "4", "0"})

        if choice == "0":
            print(t("再见。"))
            break

        if choice == "1":
            src_dirs = cfg.get("settings", {}).get("source_directories", ["D:\\Downloads"])
            if not src_dirs:
                print(t("错误：未设置来源目录，请先到设置中配置。"))
                continue
            candidates = []
            for d in src_dirs:
                f = get_latest_file(d)
                if f is not None:
                    candidates.append(f)
            if not candidates:
                print(t("所有来源目录均为空。"))
                continue
            file_path = max(candidates, key=os.path.getctime)
            organize_file(file_path, cfg)

        elif choice == "2":
            path = input(f"{t('请输入文件路径')} (0 {t('取消')}): ").strip()
            if path == "0":
                continue
            if not os.path.isfile(path):
                print(t("文件不存在。"))
                continue
            organize_file(path, cfg)

        elif choice == "3":
            manage_config(cfg)

        elif choice == "4":
            manage_settings(cfg)


if __name__ == "__main__":
    main()
