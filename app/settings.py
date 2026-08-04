import os
import json
import sys
from config import CONFIG_PATH, save_config, DEFAULT_CONFIG
import i18n
from i18n import t
from utils import input_option, input_yes_no, open_folder, split_input


def restart_app():
    """重启程序：启动新实例后退出当前进程（参数列表方式，不经过 shell）"""
    if getattr(sys, "frozen", False):
        args = [sys.executable] + sys.argv[1:]
    else:
        entry = os.environ.get("FILE_ORGANIZER_ENTRY")
        if not entry:
            entry = os.path.abspath(sys.argv[0])
        if not os.path.isfile(entry):
            print(f"{t('重启失败：找不到入口脚本')} {entry}")
            sys.exit(1)
        args = [sys.executable, entry]
    import subprocess
    try:
        subprocess.Popen(args, close_fds=True)
        sys.exit(0)
    except OSError as e:
        print(f"{t('重启失败：')}{e}")
        sys.exit(1)


# ========== 来源目录管理 ==========

def manage_source_dirs(cfg: dict):
    """三级菜单：列出来源目录 -> 选中 -> 打开/删除；[a] 新增"""
    while True:
        src = cfg["settings"]["source_directories"]
        print("\n" + "=" * 48)
        print(t("  设置来源目录"))
        print("=" * 48)

        if src:
            print(t("现有来源目录："))
            for i, d in enumerate(src, 1):
                print(f"  [{i}] {d}")
        else:
            print(t("（未设置）"))

        print(t("  [a] 新增来源目录"))
        print(t("  [0] 返回"))

        valid = {"a", "0"} | {str(i) for i in range(1, len(src) + 1)}
        choice = input_option(t("输入编号: "), valid)

        if choice == "0":
            return

        # --- 新增 ---
        if choice == "a":
            nd = input(t("请输入来源目录路径（多个用逗号分隔，0 取消）: ")).strip()
            if nd == "0" or not nd:
                continue
            added = []
            for d in split_input(nd):
                if not os.path.isabs(d):
                    print(f"{t('警告：跳过无效路径「')}{d}」")
                    continue
                if d in src:
                    print(f"{t('已存在，跳过：')}{d}")
                    continue
                src.append(d)
                added.append(d)
            if added:
                save_config(cfg)
                print(f"{t('✓ 来源目录已更新：')}{', '.join(added)}")
            continue

        # --- 选中一个目录 ---
        idx = int(choice) - 1
        dir_path = src[idx]

        while True:
            print(f"\n{dir_path}")
            print(t("  [1] 打开目录"))
            print(t("  [2] 删除此目录"))
            print(t("  [0] 取消，返回"))
            act = input_option(t("输入编号: "), {"1", "2", "0"})

            if act == "0":
                break
            if act == "1":
                open_folder(dir_path)
            elif act == "2":
                if input_yes_no(f"{t('确认删除来源目录？')}(y/n): "):
                    src.pop(idx)
                    save_config(cfg)
                    print(f"{t('✓ 已删除来源目录：')}{dir_path}")
                    break


# ========== 设置 ==========

def manage_settings(cfg: dict):
    while True:
        print("\n" + "=" * 48)
        print(t("  设置"))
        print("=" * 48)
        print(f"{t('  配置文件路径：')}")
        print(f"    {CONFIG_PATH}")
        print()
        src_dirs = cfg.get("settings", {}).get("source_directories", ["D:\\Downloads"])
        src_str = t("、").join(src_dirs) if src_dirs else t("（未设置）")
        print(f"{t('  来源目录：')}{src_str}")
        print()
        print(t("  [1] 设置来源目录"))
        print(t("  [2] 切换语言"))
        print(t("  [3] 恢复出厂设置"))
        print(t("  [0] 返回主菜单"))
        choice = input_option(t("输入编号: "), {"1", "2", "3", "0"})
        if choice == "0":
            return

        if choice == "1":
            manage_source_dirs(cfg)

        elif choice == "2":
            lang = "en" if i18n._current_lang == "zh" else "zh"
            i18n.set_language(lang)
            cfg["settings"]["language"] = lang
            save_config(cfg)
            print(t("语言已切换"))

        elif choice == "3":
            print(f"\n{t('确定要恢复出厂设置？')}")
            print(t("所有配置将被清除，此操作不可撤销。"))
            if not input_yes_no(f"{t('确认')}(y/n): "):
                continue
            if not input_yes_no(f"{t('再次确认？')}(y/n): "):
                continue
            # 直接删除配置文件，下次启动会走首次运行初始化
            try:
                if os.path.exists(CONFIG_PATH):
                    os.remove(CONFIG_PATH)
            except OSError as e:
                print(f"{t('删除配置文件失败：')}{e}")
                continue
            cfg.clear()
            i18n.set_language("zh")
            print(t("已重置为出厂状态，正在重启…"), flush=True)
            restart_app()
