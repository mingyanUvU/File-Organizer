import os
from config import CONFIG_PATH, save_config, DEFAULT_CONFIG
import i18n
from i18n import t
from utils import input_option, input_yes_no


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
            src = cfg["settings"]["source_directories"]
            if src:
                print(t("当前来源目录："))
                for i, d in enumerate(src, 1):
                    print(f"  [{i}] {d}")
            nd = input(t("请输入新来源目录（逗号分隔，0 取消）: ")).strip()
            if nd == "0":
                continue
            if nd:
                from utils import split_input
                nd_list = [d for d in split_input(nd) if os.path.isabs(d)]
                for d in split_input(nd):
                    if not os.path.isabs(d):
                        print(f"{t('警告：跳过无效路径')} {d}")
                if nd_list:
                    cfg["settings"]["source_directories"].extend(nd_list)
                    save_config(cfg)
                    print(f"{t('已添加：')}{', '.join(nd_list)}")
            if src:
                di = input(t("输入编号删除（直接回车跳过）: ")).strip()
                if di.isdigit() and 1 <= int(di) <= len(src):
                    rm = src.pop(int(di) - 1)
                    save_config(cfg)
                    print(f"{t('已删除：')}{rm}")
            print(t("来源目录已更新。"))

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
            cfg["groups"] = {}
            cfg["extensions"] = {}
            cfg["settings"]["source_directories"] = []
            cfg["settings"]["language"] = "zh"
            cfg.clear()
            cfg.update(dict(DEFAULT_CONFIG))
            save_config(cfg)
            print(t("已重置为出厂状态。"))
            from setup import first_run_setup
            first_run_setup(cfg)
            return
