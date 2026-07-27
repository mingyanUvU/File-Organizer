import os
from config import save_config
from i18n import t
from utils import (
    sanitize_folder_name, input_yes_no, input_option, open_folder, quoted
)


# ========== 管理分类 ==========

def manage_categories(cfg: dict):
    while True:
        groups = cfg["groups"]
        group_list = list(groups.keys())

        if not group_list:
            print(t("\n当前没有分组。"))
            name = input(t("新分组名 (0 返回): ")).strip()
            if not name or name == "0":
                return
            name = sanitize_folder_name(name)
            groups[name] = {}
            save_config(cfg)
            print(f"{t('✓ 已创建分组：')}{name}")
            continue

        print(t("\n--- 管理分类 ---"))
        print(t("现有分组："))
        for i, g in enumerate(group_list, 1):
            count = len(groups[g])
            print(f"  [{i}] {g}  ({count}{t(' 个分类')})")
        print(t("  [a] 新增分组"))
        g_valid = {str(i) for i in range(1, len(group_list) + 1)} | {"a", "0"}
        g_choice = input_option(t("输入编号 (0 返回): "), g_valid)
        if g_choice == "0":
            return
        if g_choice == "a":
            name = input(t("新分组名 (0 取消): ")).strip()
            if not name or name == "0":
                continue
            name = sanitize_folder_name(name)
            if name in groups:
                print(t("该分组已存在。"))
                continue
            groups[name] = {}
            save_config(cfg)
            print(f"{t('✓ 已创建分组：')}{name}")
            continue

        group_name = group_list[int(g_choice) - 1]
        cat_dict = groups[group_name]
        cat_list = list(cat_dict.keys())

        while True:
            if not cat_list:
                print(f"{group_name}{t('下没有分类。')}")
                name = input(t("新分类名 (0 返回分组列表): ")).strip()
                if not name or name == "0":
                    break
                name = sanitize_folder_name(name)
                path_input = input(t("目标路径（可选）: ")).strip()
                cat_dict[name] = path_input
                save_config(cfg)
                print(f"{t('✓ 已创建分类：')}{name}")
                cat_list = list(cat_dict.keys())
                continue

            print(f"\n{group_name}{t(' 下的分类：')}")
            for i, c in enumerate(cat_list, 1):
                path_hint = cat_dict[c] if cat_dict[c] else t("（未设置）")
                print(f"  [{i}] {c}  {t('→')}  {path_hint}")
            print(t("  [a] 新增分类"))
            c_valid = {str(i) for i in range(1, len(cat_list) + 1)} | {"a", "0"}
            c_choice = input_option(t("输入编号 (0 返回分组列表): "), c_valid)
            if c_choice == "0":
                break
            if c_choice == "a":
                name = input(t("新分类名 (0 取消): ")).strip()
                if not name or name == "0":
                    continue
                name = sanitize_folder_name(name)
                if name in cat_dict:
                    print(t("该分类已存在。"))
                    continue
                path_input = input(t("目标路径（可选）: ")).strip()
                cat_dict[name] = path_input
                save_config(cfg)
                print(f"{t('✓ 已创建分类：')}{name}")
                cat_list = list(cat_dict.keys())
                continue

            cat_name = cat_list[int(c_choice) - 1]
            current_path = cat_dict[cat_name]

            # 操作菜单
            while True:
                path_display = current_path if current_path else t("（未设置）")
                print(f"\n{cat_name} ({group_name})")
                print(f"{t('  路径：')}{path_display}\n")
                print(t("  [1] 修改路径"))
                print(t("  [2] 重命名"))
                print(t("  [3] 移动到其他分组"))
                print(t("  [4] 删除"))
                print(t("  [5] 打开目标文件夹"))
                act = input_option(t("输入编号 (0 取消): "), {"1", "2", "3", "4", "5", "0"})
                if act == "0":
                    break

                if act == "1":
                    new_path = input(t("新路径 (0 取消): ")).strip()
                    if new_path == "0":
                        continue
                    if not os.path.isabs(new_path):
                        print(t("请输入绝对路径。"))
                        continue
                    cat_dict[cat_name] = new_path
                    current_path = new_path
                    save_config(cfg)
                    print(t("路径已更新。"))

                elif act == "2":
                    new_name = input(t("新名称 (0 取消): ")).strip()
                    if not new_name or new_name == "0":
                        continue
                    new_name = sanitize_folder_name(new_name)
                    if new_name == cat_name:
                        print(t("名称未变化。"))
                        continue
                    if new_name in cat_dict:
                        print(t("该名称已存在。"))
                        continue
                    cat_dict[new_name] = cat_dict.pop(cat_name)
                    for ext, mappings in cfg["extensions"].items():
                        for i, (g, c) in enumerate(mappings):
                            if g == group_name and c == cat_name:
                                mappings[i][1] = new_name
                    save_config(cfg)
                    print(f"{t('已重命名为：')}{new_name}")
                    cat_name = new_name
                    cat_list = list(cat_dict.keys())

                elif act == "3":
                    other_groups = [g for g in groups if g != group_name]
                    if not other_groups:
                        print(t("没有其他分组可移动。"))
                        continue
                    print(t("目标分组："))
                    for i, g in enumerate(other_groups, 1):
                        print(f"  [{i}] {g}")
                    tg = input_option(t("输入编号 (0 取消): "),
                                      {str(i) for i in range(1, len(other_groups) + 1)} | {"0"})
                    if tg == "0":
                        continue
                    target_group = other_groups[int(tg) - 1]
                    groups[target_group][cat_name] = cat_dict.pop(cat_name)
                    for ext, mappings in cfg["extensions"].items():
                        for i, (g, c) in enumerate(mappings):
                            if g == group_name and c == cat_name:
                                mappings[i][0] = target_group
                    save_config(cfg)
                    print(f"{t('已移动到分组：')}{target_group}")
                    cat_list = list(cat_dict.keys())
                    break

                elif act == "4":
                    ref_count = sum(1 for mappings in cfg["extensions"].values()
                                    for g, c in mappings
                                    if g == group_name and c == cat_name)
                    if ref_count > 0:
                        print(f"{t('该分类下有')}{ref_count}{t('条后缀映射引用，删除后这些映射也会被移除。')}")
                    if input_yes_no(f"{t('确认删除分类')}{cat_name}？(y/n): "):
                        del cat_dict[cat_name]
                        for ext in list(cfg["extensions"].keys()):
                            cfg["extensions"][ext] = [
                                m for m in cfg["extensions"][ext]
                                if not (m[0] == group_name and m[1] == cat_name)
                            ]
                            if not cfg["extensions"][ext]:
                                del cfg["extensions"][ext]
                        save_config(cfg)
                        print(t("已删除。"))
                        cat_list = list(cat_dict.keys())
                        break

                elif act == "5":
                    if current_path:
                        open_folder(current_path)
                    else:
                        print(t("未设置路径。"))
