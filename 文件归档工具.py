import os
import sys
import shutil
import json
import time
from datetime import datetime


# ========== 路径配置 ==========

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_PATH = os.path.join(BASE_DIR, "分类配置.json")

DEFAULT_CONFIG = {
    "version": 1,
    "settings": {
        "source_directories": ["D:\\Downloads"]
    },
    "groups": {
        "AI Draw": {
            "绘画模型": R"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\models\Stable-diffusion",
            "Lora":      R"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\models\Lora",
            "VAE":       R"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\models\VAE",
            "Embedding": R"D:\AAAMyApp\AI\sd-webui-aki-v4.11.1-cu128\embeddings"
        },
        "默认分类": {}
    },
    "extensions": {
        ".safetensors": [["AI Draw", "绘画模型"]],
        ".ckpt":        [["AI Draw", "绘画模型"]],
        ".pt":          [["AI Draw", "VAE"]],
        ".png":         [["默认分类", "图片"]],
        ".jpg":         [["默认分类", "图片"]],
        ".jpeg":        [["默认分类", "图片"]],
        ".webp":        [["默认分类", "图片"]],
        ".pdf":         [["默认分类", "文档"]],
        ".docx":        [["默认分类", "文档"]],
        ".xlsx":        [["默认分类", "文档"]],
        ".txt":         [["默认分类", "文档"]],
        ".zip":         [["默认分类", "压缩包"]],
        ".rar":         [["默认分类", "压缩包"]],
        ".7z":          [["默认分类", "压缩包"]]
    }
}


# ========== 配置读写 ==========

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        config = dict(DEFAULT_CONFIG)
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    # 确保 settings 字段兼容旧配置
    if "settings" not in config:
        config["settings"] = {"source_directories": ["D:\\Downloads"]}
    return config


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ========== 工具函数 ==========

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
        print("输入无效，请输入 y/n")


def input_option(prompt: str, valid_options: set) -> str:
    while True:
        val = input(prompt).strip().lower()
        if val in valid_options:
            return val
        print(f"输入无效，请输入 {'/'.join(sorted(valid_options, key=lambda x: (x.isdigit(), x)))}")


def open_folder(path: str):
    if os.path.isdir(path):
        os.startfile(path)
    else:
        print(f"路径不存在：{path}")


def get_latest_file(folder: str) -> str | None:
    if not os.path.isdir(folder):
        print(f"错误：目录不存在 — {folder}")
        return None
    entries = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]
    if not entries:
        print("目录为空，没有可处理的文件。")
        return None
    return max(entries, key=os.path.getctime)


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def show_file_info(file_path: str):
    stat = os.stat(file_path)
    ctime = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"  文件名：{os.path.basename(file_path)}")
    print(f"  后缀名：{os.path.splitext(file_path)[1].lower()}")
    print(f"  大小：{format_size(stat.st_size)}")
    print(f"  加入时间：{ctime}")


# ========== 分类选择（分组→分类 两级菜单） ==========

def select_classification(cfg: dict, prompt: str = "请选择分类") -> tuple | None:
    """
    返回 (group_name, category_name) 或 None（取消）
    """
    groups = cfg["groups"]

    # --- 选分组 ---
    group_list = list(groups.keys())
    print(f"\n--- {prompt} ---")
    print("选择分组：")
    for i, g in enumerate(group_list, 1):
        print(f"  [{i}] {g}")
    print("  [a] 新增分组")
    g_valid = {str(i) for i in range(1, len(group_list) + 1)} | {"a", "0"}
    g_choice = input_option("输入编号 (0 取消): ", g_valid)
    if g_choice == "0":
        return None
    if g_choice == "a":
        # 新增分组
        name = input("新分组名 (0 取消): ").strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        if name in groups:
            print("该分组已存在。")
            return None
        groups[name] = {}
        save_config(cfg)
        print(f"✓ 已创建分组：{name}")
        group_name = name
    else:
        group_name = group_list[int(g_choice) - 1]

    # --- 选分类 ---
    cat_dict = groups[group_name]
    cat_list = list(cat_dict.keys())
    if not cat_list:
        print(f"分组「{group_name}」下没有分类，请先新增。")
        # 直接进入新增
        name = input("新分类名 (0 取消): ").strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        path_input = input("目标路径（可选，留空后续设置）: ").strip()
        cat_dict[name] = path_input
        save_config(cfg)
        print(f"✓ 已创建分类：{group_name} → {name}")
        return group_name, name

    print(f"\n{group_name} 下的分类：")
    for i, c in enumerate(cat_list, 1):
        path_hint = cat_dict[c] if cat_dict[c] else "（未设置）"
        print(f"  [{i}] {c}  →  {path_hint}")
    print("  [a] 新增分类")
    c_valid = {str(i) for i in range(1, len(cat_list) + 1)} | {"a", "0"}
    c_choice = input_option("输入编号 (0 返回): ", c_valid)
    if c_choice == "0":
        return None
    if c_choice == "a":
        name = input("新分类名 (0 取消): ").strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        if name in cat_dict:
            print("该分类已存在。")
            return None
        path_input = input("目标路径（可选，留空后续设置）: ").strip()
        cat_dict[name] = path_input
        save_config(cfg)
        print(f"✓ 已创建分类：{group_name} → {name}")
        return group_name, name
    else:
        cat_name = cat_list[int(c_choice) - 1]
        return group_name, cat_name


# ========== 核心整理流程 ==========

def organize_file(file_path: str, cfg: dict):
    if not os.path.isfile(file_path):
        print("错误：文件不存在。")
        return

    print("\n" + "=" * 48)
    show_file_info(file_path)
    print("=" * 48)

    ext = os.path.splitext(file_path)[1].lower()
    ext_mappings = cfg["extensions"].get(ext, [])

    # 决定目标 (group_name, cat_name)
    target = None

    if len(ext_mappings) == 0:
        # 未知后缀，列出所有分类
        print(f"\n未识别的后缀「{ext}」，请从所有分类中选择：")
        target = select_classification(cfg, "从所有分类中选择")
        if target is None:
            return

    elif len(ext_mappings) == 1:
        g, c = ext_mappings[0]
        cat_path = cfg["groups"].get(g, {}).get(c, "")
        label = f"{g} → {c}"
        print(f"\n建议分类：{label}  ({cat_path})")
        if input_yes_no("是否使用此分类？(y/n): "):
            target = (g, c)
        else:
            target = select_classification(cfg, "请重新选择分类")
            if target is None:
                return

    else:
        print(f"\n后缀「{ext}」有 {len(ext_mappings)} 个指向：")
        for i, (g, c) in enumerate(ext_mappings, 1):
            cat_path = cfg["groups"].get(g, {}).get(c, "")
            print(f"  [{i}] {g} → {c}  ({cat_path})")
        print("  [0] 从所有分类中选择")
        m_valid = {str(i) for i in range(1, len(ext_mappings) + 1)} | {"0"}
        m_choice = input_option("输入编号: ", m_valid)
        if m_choice == "0":
            target = select_classification(cfg, "从所有分类中选择")
            if target is None:
                return
        else:
            target = ext_mappings[int(m_choice) - 1]

    group_name, cat_name = target
    cat_path = cfg["groups"].get(group_name, {}).get(cat_name, "")

    # 检查路径是否已设置
    if not cat_path:
        print(f"\n分类「{group_name} → {cat_name}」未设置目标路径。")
        set_now = input_yes_no("现在设置？(y/n): ")
        if set_now:
            new_path = input("请输入路径: ").strip()
            if not os.path.isabs(new_path):
                print("路径无效，请使用绝对路径。")
                return
            cfg["groups"][group_name][cat_name] = new_path
            save_config(cfg)
            cat_path = new_path
        else:
            print("取消操作。")
            return

    # 文件夹命名
    default_name = sanitize_folder_name(os.path.splitext(os.path.basename(file_path))[0])
    folder_input = input(f"文件夹名（直接回车默认：{default_name}）: ").strip()
    folder_name = sanitize_folder_name(folder_input) if folder_input else default_name
    if not folder_name:
        print("名称无效，使用默认名。")
        folder_name = default_name

    target_dir = os.path.join(cat_path, folder_name)

    # 移动
    try:
        os.makedirs(target_dir, exist_ok=True)
        dst = os.path.join(target_dir, os.path.basename(file_path))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(file_path, target_dir)
        print(f"\n✓ 已移动到：{group_name} → {cat_name} → {folder_name}")
    except Exception as e:
        print(f"移动失败：{e}")
        return

    if input_yes_no("是否打开目标文件夹？(y/n): "):
        open_folder(target_dir)


# ========== 管理分类 ==========

def manage_categories(cfg: dict):
    while True:
        groups = cfg["groups"]
        group_list = list(groups.keys())

        if not group_list:
            print("\n当前没有分组。")
            name = input("新分组名 (0 返回): ").strip()
            if not name or name == "0":
                return
            name = sanitize_folder_name(name)
            groups[name] = {}
            save_config(cfg)
            print(f"✓ 已创建分组：{name}")
            continue

        print("\n--- 管理分类 ---")
        print("现有分组：")
        for i, g in enumerate(group_list, 1):
            count = len(groups[g])
            print(f"  [{i}] {g}  ({count} 个分类)")
        print("  [a] 新增分组")
        g_valid = {str(i) for i in range(1, len(group_list) + 1)} | {"a", "0"}
        g_choice = input_option("输入编号 (0 返回): ", g_valid)
        if g_choice == "0":
            return
        if g_choice == "a":
            name = input("新分组名 (0 取消): ").strip()
            if not name or name == "0":
                continue
            name = sanitize_folder_name(name)
            if name in groups:
                print("该分组已存在。")
                continue
            groups[name] = {}
            save_config(cfg)
            print(f"✓ 已创建分组：{name}")
            continue

        group_name = group_list[int(g_choice) - 1]
        cat_dict = groups[group_name]
        cat_list = list(cat_dict.keys())

        while True:
            if not cat_list:
                print(f"\n分组「{group_name}」下没有分类。")
                name = input("新分类名 (0 返回分组列表): ").strip()
                if not name or name == "0":
                    break
                name = sanitize_folder_name(name)
                path_input = input("目标路径（可选）: ").strip()
                cat_dict[name] = path_input
                save_config(cfg)
                print(f"✓ 已创建分类：{name}")
                cat_list = list(cat_dict.keys())
                if not cat_list:
                    break
                continue

            print(f"\n{group_name} 下的分类：")
            for i, c in enumerate(cat_list, 1):
                path_hint = cat_dict[c] if cat_dict[c] else "（未设置）"
                print(f"  [{i}] {c}  →  {path_hint}")
            print("  [a] 新增分类")
            c_valid = {str(i) for i in range(1, len(cat_list) + 1)} | {"a", "0"}
            c_choice = input_option("输入编号 (0 返回分组列表): ", c_valid)
            if c_choice == "0":
                break
            if c_choice == "a":
                name = input("新分类名 (0 取消): ").strip()
                if not name or name == "0":
                    continue
                name = sanitize_folder_name(name)
                if name in cat_dict:
                    print("该分类已存在。")
                    continue
                path_input = input("目标路径（可选）: ").strip()
                cat_dict[name] = path_input
                save_config(cfg)
                print(f"✓ 已创建分类：{name}")
                cat_list = list(cat_dict.keys())
                continue

            cat_name = cat_list[int(c_choice) - 1]
            current_path = cat_dict[cat_name]

            # --- 分类操作菜单 ---
            while True:
                path_display = current_path if current_path else "（未设置）"
                print(f"\n{cat_name} ({group_name})")
                print(f"  路径：{path_display}")
                print()
                print("  [1] 修改路径")
                print("  [2] 重命名")
                print("  [3] 移动到其他分组")
                print("  [4] 删除")
                print("  [5] 打开目标文件夹")
                act_valid = {"1", "2", "3", "4", "5", "0"}
                act = input_option("输入编号 (0 取消): ", act_valid)

                if act == "0":
                    break

                if act == "1":
                    new_path = input("新路径 (0 取消): ").strip()
                    if new_path == "0":
                        continue
                    if not os.path.isabs(new_path):
                        print("请输入绝对路径。")
                        continue
                    cat_dict[cat_name] = new_path
                    current_path = new_path
                    save_config(cfg)
                    print("✓ 路径已更新。")

                elif act == "2":
                    new_name = input("新名称 (0 取消): ").strip()
                    if not new_name or new_name == "0":
                        continue
                    new_name = sanitize_folder_name(new_name)
                    if new_name == cat_name:
                        print("名称未变化。")
                        continue
                    if new_name in cat_dict:
                        print("该名称已存在。")
                        continue
                    # 更新此分类在 extensions 里的引用
                    cat_dict[new_name] = cat_dict.pop(cat_name)
                    for ext, mappings in cfg["extensions"].items():
                        for i, (g, c) in enumerate(mappings):
                            if g == group_name and c == cat_name:
                                mappings[i][1] = new_name
                    save_config(cfg)
                    print(f"✓ 已重命名为：{new_name}")
                    cat_name = new_name
                    cat_list = list(cat_dict.keys())

                elif act == "3":
                    other_groups = [g for g in groups if g != group_name]
                    if not other_groups:
                        print("没有其他分组可移动。")
                        continue
                    print("目标分组：")
                    for i, g in enumerate(other_groups, 1):
                        print(f"  [{i}] {g}")
                    tg_valid = {str(i) for i in range(1, len(other_groups) + 1)} | {"0"}
                    tg = input_option("输入编号 (0 取消): ", tg_valid)
                    if tg == "0":
                        continue
                    target_group = other_groups[int(tg) - 1]
                    # 移到目标组
                    groups[target_group][cat_name] = cat_dict.pop(cat_name)
                    # 更新 extensions 里的引用
                    for ext, mappings in cfg["extensions"].items():
                        for i, (g, c) in enumerate(mappings):
                            if g == group_name and c == cat_name:
                                mappings[i][0] = target_group
                    save_config(cfg)
                    print(f"✓ 已移动到分组：{target_group}")
                    cat_list = list(cat_dict.keys())
                    break  # 返回分类列表

                elif act == "4":
                    # 删除前检查引用
                    ref_count = sum(
                        1 for mappings in cfg["extensions"].values()
                        for g, c in mappings
                        if g == group_name and c == cat_name
                    )
                    warn = f"该分类下有 {ref_count} 条后缀映射引用，删除后这些映射也会被移除。"
                    if ref_count > 0:
                        print(warn)
                    if input_yes_no(f"确认删除分类「{cat_name}」？(y/n): "):
                        del cat_dict[cat_name]
                        # 清理 extensions 里的引用
                        for ext in list(cfg["extensions"].keys()):
                            cfg["extensions"][ext] = [
                                m for m in cfg["extensions"][ext]
                                if not (m[0] == group_name and m[1] == cat_name)
                            ]
                            if not cfg["extensions"][ext]:
                                del cfg["extensions"][ext]
                        save_config(cfg)
                        print("✓ 已删除。")
                        cat_list = list(cat_dict.keys())
                        break  # 返回分类列表

                elif act == "5":
                    if current_path:
                        open_folder(current_path)
                    else:
                        print("未设置路径。")


# ========== 管理后缀映射 ==========

def manage_extensions(cfg: dict):
    while True:
        ext_dict = cfg["extensions"]
        ext_list = sorted(ext_dict.keys())

        if not ext_list:
            print("\n当前没有后缀映射。")
        else:
            print("\n--- 管理后缀映射 ---")
            print("现有后缀：")
            for i, ext in enumerate(ext_list, 1):
                count = len(ext_dict[ext])
                print(f"  [{i}] {ext}  ({count} 个指向)")

        print("  [a] 新增后缀映射")
        e_valid = {str(i) for i in range(1, len(ext_list) + 1)} | {"a", "0"}
        e_choice = input_option("输入编号 (0 返回): ", e_valid)
        if e_choice == "0":
            return

        # --- 新增后缀 ---
        if e_choice == "a":
            ext = input("请输入后缀名（如 .png，0 取消）: ").strip().lower()
            if ext == "0" or not ext:
                continue
            if not ext.startswith("."):
                ext = "." + ext

            if ext in ext_dict:
                print(f"后缀 {ext} 已存在，将添加新的指向。")

            # 循环添加多条映射
            if ext not in ext_dict:
                ext_dict[ext] = []

            while True:
                result = select_classification(cfg, f"为 {ext} 选择指向")
                if result is None:
                    break
                g, c = result
                ext_dict[ext].append([g, c])
                save_config(cfg)
                print(f"✓ 已添加：{ext} → {g} → {c}")
                if not input_yes_no("是否继续添加指向？(y/n): "):
                    break
            continue

        # --- 选择后缀 ---
        ext = ext_list[int(e_choice) - 1]
        mappings = ext_dict[ext]

        while True:
            print(f"\n{ext}")
            print("  现有映射：")
            for i, (g, c) in enumerate(mappings, 1):
                cat_path = cfg["groups"].get(g, {}).get(c, "")
                hint = f"  ({cat_path})" if cat_path else ""
                print(f"    [{i}] {g} → {c} {hint}")
            print()
            print("  [a] 新增映射")
            print("  [b] 删除整个后缀")

            # 选择单条映射或操作
            m_valid = {str(i) for i in range(1, len(mappings) + 1)} | {"a", "b", "0"}
            m_choice = input_option("输入编号 (0 返回): ", m_valid)

            if m_choice == "0":
                break

            if m_choice == "a":
                result = select_classification(cfg, f"为 {ext} 新增指向")
                if result is None:
                    continue
                g, c = result
                mappings.append([g, c])
                save_config(cfg)
                print(f"✓ 已添加：{ext} → {g} → {c}")
                continue

            if m_choice == "b":
                if input_yes_no(f"确认删除后缀 {ext} 的所有映射？(y/n): "):
                    del ext_dict[ext]
                    save_config(cfg)
                    print("✓ 已删除。")
                    break
                continue

            # --- 选中单条映射的操作 ---
            g, c = mappings[int(m_choice) - 1]
            cat_path = cfg["groups"].get(g, {}).get(c, "")

            while True:
                path_display = cat_path if cat_path else "（未设置）"
                print(f"\n{g} → {c}")
                print(f"  路径：{path_display}")
                print()
                print("  [1] 修改指向")
                print("  [2] 打开目标文件夹")
                print("  [3] 删除此条映射")
                m_act_valid = {"1", "2", "3", "0"}
                m_act = input_option("输入编号 (0 取消): ", m_act_valid)

                if m_act == "0":
                    break

                if m_act == "1":
                    result = select_classification(cfg, "选择新指向")
                    if result is None:
                        continue
                    ng, nc = result
                    mappings[int(m_choice) - 1] = [ng, nc]
                    save_config(cfg)
                    print(f"✓ 已修改：{ext} → {ng} → {nc}")
                    g, c = ng, nc
                    cat_path = cfg["groups"].get(g, {}).get(c, "")

                elif m_act == "2":
                    if cat_path:
                        open_folder(cat_path)
                    else:
                        print("未设置路径。")

                elif m_act == "3":
                    if input_yes_no("确认删除此条映射？(y/n): "):
                        mappings.pop(int(m_choice) - 1)
                        if not mappings:
                            del ext_dict[ext]
                        save_config(cfg)
                        print("✓ 已删除。")
                        break  # 回到后缀详情


# ========== 配置管理主菜单 ==========

def manage_config(cfg: dict):
    while True:
        print("\n" + "=" * 48)
        print("  配置管理")
        print("=" * 48)
        print("  [1] 管理分类")
        print("  [2] 管理后缀映射")
        print("  [0] 返回主菜单")
        choice = input_option("输入编号: ", {"1", "2", "0"})
        if choice == "0":
            return
        if choice == "1":
            manage_categories(cfg)
        elif choice == "2":
            manage_extensions(cfg)


# ========== 设置 ==========

def manage_settings(cfg: dict):
    while True:
        print("\n" + "=" * 48)
        print("  设置")
        print("=" * 48)
        print("  配置文件路径：")
        print(f"    {CONFIG_PATH}")
        print()
        src_dirs = cfg.get("settings", {}).get("source_directories", ["D:\\Downloads"])
        src_str = "、".join(src_dirs) if src_dirs else "（未设置）"
        print("  来源目录：")
        print(f"    {src_str}")
        print()
        print("  [1] 设置来源目录")
        print("  [0] 返回主菜单")
        choice = input_option("输入编号: ", {"1", "0"})
        if choice == "0":
            return
        if choice == "1":
            new_dir = input("请输入来源目录路径 (多个用逗号分隔，0 取消): ").strip()
            if new_dir == "0" or not new_dir:
                continue
            dirs = [d.strip() for d in new_dir.split(",") if d.strip()]
            valid_dirs = []
            for d in dirs:
                if os.path.isabs(d):
                    valid_dirs.append(d)
                else:
                    print(f"警告：跳过无效路径「{d}」，请使用绝对路径。")
            if valid_dirs:
                cfg["settings"]["source_directories"] = valid_dirs
                save_config(cfg)
                print(f"✓ 来源目录已更新：{'、'.join(valid_dirs)}")
            else:
                print("未设置有效的目录。")


# ========== 主菜单 ==========

def main():
    # 控制台编码
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)

    cfg = load_config()

    while True:
        print("\n" + "=" * 48)
        print("  文件归档工具")
        print("=" * 48)
        print("  [1] 整理最新下载文件")
        print("  [2] 移动指定文件")
        print("  [3] 管理分类配置")
        print("  [4] 设置")
        print("  [0] 退出")
        choice = input_option("输入编号: ", {"1", "2", "3", "4", "0"})

        if choice == "0":
            print("再见。")
            break

        if choice == "1":
            src_dirs = cfg.get("settings", {}).get("source_directories", ["D:\\Downloads"])
            if not src_dirs:
                print("错误：未设置来源目录，请先到设置中配置。")
                continue
            file_path = get_latest_file(src_dirs[0])
            if file_path is None:
                continue
            organize_file(file_path, cfg)

        elif choice == "2":
            path = input("请输入文件路径 (0 取消): ").strip()
            if path == "0":
                continue
            if not os.path.isfile(path):
                print("错误：文件不存在。")
                continue
            organize_file(path, cfg)

        elif choice == "3":
            manage_config(cfg)

        elif choice == "4":
            manage_settings(cfg)

if __name__ == "__main__":
    main()
