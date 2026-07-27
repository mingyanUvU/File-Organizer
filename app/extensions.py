import os
from config import save_config
from i18n import t
from utils import (
    input_yes_no, input_option, open_folder, select_classification, quoted
)


# ========== 管理后缀映射 ==========

def manage_extensions(cfg: dict):
    while True:
        ext_dict = cfg["extensions"]
        ext_list = sorted(ext_dict.keys())

        if not ext_list:
            print(t("\n当前没有后缀映射。"))
        else:
            print(t("\n--- 管理后缀映射 ---"))
            print(t("现有后缀："))
            for i, ext in enumerate(ext_list, 1):
                count = len(ext_dict[ext])
                print(f"  [{i}] {ext}  ({count}{t(' 个指向')})")

        print(t("  [a] 新增后缀映射"))
        e_valid = {str(i) for i in range(1, len(ext_list) + 1)} | {"a", "0"}
        e_choice = input_option(t("输入编号 (0 返回): "), e_valid)
        if e_choice == "0":
            return

        if e_choice == "a":
            ext = input(t("请输入后缀名（如 .png，0 取消）: ")).strip().lower()
            if ext == "0" or not ext:
                continue
            if not ext.startswith("."):
                ext = "." + ext
            if ext in ext_dict:
                print(t("该后缀已存在，将添加新的指向。"))
            if ext not in ext_dict:
                ext_dict[ext] = []
            while True:
                result = select_classification(cfg, f"{ext}{t('选择新指向')}")
                if result is None:
                    break
                g, c = result
                ext_dict[ext].append([g, c])
                save_config(cfg)
                print(f"{t('✓ 已添加：')}{ext} {t('→')} {quoted(g)} {t('→')} {quoted(c)}")
                if not input_yes_no(t("是否继续添加指向？(y/n): ")):
                    break
            continue

        ext = ext_list[int(e_choice) - 1]
        mappings = ext_dict[ext]

        while True:
            print(f"\n{ext}")
            print(t("  现有映射："))
            for i, (g, c) in enumerate(mappings, 1):
                cat_path = cfg["groups"].get(g, {}).get(c, "")
                hint = f"  ({cat_path})" if cat_path else ""
                print(f"    [{i}] {quoted(g)} {t('→')} {quoted(c)} {hint}")
            print(t("  [a] 新增映射"))
            print(t("  [b] 删除整个后缀"))

            m_valid = {str(i) for i in range(1, len(mappings) + 1)} | {"a", "b", "0"}
            m_choice = input_option(t("输入编号 (0 返回): "), m_valid)
            if m_choice == "0":
                break

            if m_choice == "a":
                result = select_classification(cfg, f"{ext}{t('选择新指向')}")
                if result is None:
                    continue
                g, c = result
                mappings.append([g, c])
                save_config(cfg)
                print(f"{t('✓ 已添加：')}{ext} {t('→')} {quoted(g)} {t('→')} {quoted(c)}")
                continue

            if m_choice == "b":
                if input_yes_no(f"{t('确认删除后缀')} {ext}{t(' 的所有映射？(y/n): ')}"):
                    del ext_dict[ext]
                    save_config(cfg)
                    print(t("已删除。"))
                    break
                continue

            # 单条映射操作
            g, c = mappings[int(m_choice) - 1]
            cat_path = cfg["groups"].get(g, {}).get(c, "")

            while True:
                path_display = cat_path if cat_path else t("（未设置）")
                print(f"\n{quoted(g)} {t('→')} {quoted(c)}")
                print(f"{t('  路径：')}{path_display}\n")
                print(t("  [1] 修改指向"))
                print(t("  [2] 打开目标文件夹"))
                print(t("  [3] 删除此条映射"))
                m_act = input_option(t("输入编号 (0 取消): "), {"1", "2", "3", "0"})
                if m_act == "0":
                    break

                if m_act == "1":
                    result = select_classification(cfg, t("选择新指向"))
                    if result is None:
                        continue
                    ng, nc = result
                    mappings[int(m_choice) - 1] = [ng, nc]
                    save_config(cfg)
                    print(f"{t('✓ 已修改：')}{ext} {t('→')} {ng} {t('→')} {quoted(nc)}")
                    g, c = ng, nc
                    cat_path = cfg["groups"].get(g, {}).get(c, "")

                elif m_act == "2":
                    if cat_path:
                        open_folder(cat_path)
                    else:
                        print(t("未设置路径。"))

                elif m_act == "3":
                    if input_yes_no(t("删除此条映射？(y/n): ")):
                        mappings.pop(int(m_choice) - 1)
                        if not mappings:
                            del ext_dict[ext]
                        save_config(cfg)
                        print(t("已删除。"))
                        break
