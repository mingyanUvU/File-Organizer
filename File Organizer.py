import os
import sys
import shutil
import json
import time
from datetime import datetime


# ========== 路径配置 ==========

# ========== 国际化 ==========

_current_lang = "zh"

_T = {
    "输入无效，请输入 y/n": ["输入无效，请输入 y/n", "输入无效，请输入 y/n"],
    "目录为空，没有可处理的文件。": ["目录为空，没有可处理的文件。", "目录为空，没有可处理的文件。"],
    "选择分组：": ["选择分组：", "Select group:"],
    "  [a] 新增分组": ["  [a] 新增分组", "  [a] 新增分组"],
    "新分组名 (0 取消): ": ["新分组名 (0 取消): ", "新分组名 (0 取消): "],
    "该分组已存在。": ["该分组已存在。", "Group already exists."],
    "新分类名 (0 取消): ": ["新分类名 (0 取消): ", "新分类名 (0 取消): "],
    "目标路径（可选，留空后续设置）: ": ["目标路径（可选，留空后续设置）: ", "目标路径（可选，留空后续设置）: "],
    "  [a] 新增分类": ["  [a] 新增分类", "  [a] 新增分类"],
    "该分类已存在。": ["该分类已存在。", "Category already exists."],
    "错误：文件不存在。": ["错误：文件不存在。", "错误：文件不存在。"],
    "  [0] 从所有分类中选择": ["  [0] 从所有分类中选择", "  [0] 从所有分类中选择"],
    "请输入路径: ": ["请输入路径: ", "请输入路径: "],
    "路径无效，请使用绝对路径。": ["路径无效，请使用绝对路径。", "路径无效，请使用绝对路径。"],
    "取消操作。": ["取消操作。", "Operation cancelled."],
    "名称无效，使用默认名。": ["名称无效，使用默认名。", "Invalid name, using default."],
    "\n当前没有分组。": ["\n当前没有分组。", "\n当前没有分组。"],
    "新分组名 (0 返回): ": ["新分组名 (0 返回): ", "新分组名 (0 返回): "],
    "\n--- 管理分类 ---": ["\n--- 管理分类 ---", "\n--- 管理分类 ---"],
    "现有分组：": ["现有分组：", "Existing Groups:"],
    "新分类名 (0 返回分组列表): ": ["新分类名 (0 返回分组列表): ", "新分类名 (0 返回分组列表): "],
    "目标路径（可选）: ": ["目标路径（可选）: ", "目标路径（可选）: "],
    "  [1] 修改路径": ["  [1] 修改路径", "  [1] 修改路径"],
    "  [2] 重命名": ["  [2] 重命名", "  [2] 重命名"],
    "  [3] 移动到其他分组": ["  [3] 移动到其他分组", "  [3] 移动到其他分组"],
    "  [4] 删除": ["  [4] 删除", "  [4] 删除"],
    "  [5] 打开目标文件夹": ["  [5] 打开目标文件夹", "  [5] 打开目标文件夹"],
    "新路径 (0 取消): ": ["新路径 (0 取消): ", "新路径 (0 取消): "],
    "请输入绝对路径。": ["请输入绝对路径。", "Please use absolute path."],
    "✓ 路径已更新。": ["✓ 路径已更新。", "✓ 路径已更新。"],
    "新名称 (0 取消): ": ["新名称 (0 取消): ", "新名称 (0 取消): "],
    "名称未变化。": ["名称未变化。", "Name unchanged."],
    "该名称已存在。": ["该名称已存在。", "Name already exists."],
    "没有其他分组可移动。": ["没有其他分组可移动。", "No other groups to move to."],
    "目标分组：": ["目标分组：", "目标分组："],
    "✓ 已删除。": ["✓ 已删除。", "✓ 已删除。"],
    "未设置路径。": ["未设置路径。", "Path not set."],
    "\n当前没有后缀映射。": ["\n当前没有后缀映射。", "\n当前没有后缀映射。"],
    "\n--- 管理后缀映射 ---": ["\n--- 管理后缀映射 ---", "\n--- 管理后缀映射 ---"],
    "现有后缀：": ["现有后缀：", "现有后缀："],
    "  [a] 新增后缀映射": ["  [a] 新增后缀映射", "  [a] 新增后缀映射"],
    "请输入后缀名（如 .png，0 取消）: ": ["请输入后缀名（如 .png，0 取消）: ", "请输入后缀名（如 .png，0 取消）: "],
    "  现有映射：": ["  现有映射：", "  现有映射："],
    "  [a] 新增映射": ["  [a] 新增映射", "  [a] 新增映射"],
    "  [b] 删除整个后缀": ["  [b] 删除整个后缀", "  [b] 删除整个后缀"],
    "  [1] 修改指向": ["  [1] 修改指向", "  [1] 修改指向"],
    "  [2] 打开目标文件夹": ["  [2] 打开目标文件夹", "  [2] 打开目标文件夹"],
    "  [3] 删除此条映射": ["  [3] 删除此条映射", "  [3] 删除此条映射"],
    "  配置管理": ["  配置管理", "  配置管理"],
    "  [1] 管理分类": ["  [1] 管理分类", "  [1] 管理分类"],
    "  [2] 管理后缀映射": ["  [2] 管理后缀映射", "  [2] 管理后缀映射"],
    "  [0] 返回主菜单": ["  [0] 返回主菜单", "  [0] 返回主菜单"],
    "  设置": ["  设置", "  设置"],
    "  配置文件路径：": ["  配置文件路径：", "  配置文件路径："],
    "  来源目录：": ["  来源目录：", "  来源目录："],
    "  [1] 设置来源目录": ["  [1] 设置来源目录", "  [1] 设置来源目录"],
    "请输入来源目录路径 (多个用逗号分隔，0 取消): ": ["请输入来源目录路径 (多个用逗号分隔，0 取消): ", "请输入来源目录路径 (多个用逗号分隔，0 取消): "],
    "未设置有效的目录。": ["未设置有效的目录。", "未设置有效的目录。"],
    "  文件归档工具": ["  文件归档工具", "  文件归档工具"],
    "  [1] 整理最新下载文件": ["  [1] 整理最新下载文件", "  [1] 整理最新下载文件"],
    "  [2] 移动指定文件": ["  [2] 移动指定文件", "  [2] 移动指定文件"],
    "  [3] 管理分类配置": ["  [3] 管理分类配置", "  [3] 管理分类配置"],
    "  [4] 设置": ["  [4] 设置", "  [4] 设置"],
    "  [0] 退出": ["  [0] 退出", "  [0] 退出"],
    "再见。": ["再见。", "Goodbye."],
    "错误：未设置来源目录，请先到设置中配置。": ["错误：未设置来源目录，请先到设置中配置。", "错误：未设置来源目录，请先到设置中配置。"],
    "所有来源目录均为空。": ["所有来源目录均为空。", "All source directories are empty."],
    "请输入文件路径 (0 取消): ": ["请输入文件路径 (0 取消): ", "请输入文件路径 (0 取消): "],
    "s000": ["路径不存在：{path}", "路径不存在：{path}"],
    "s001": ["错误：目录不存在 — {folder}", "错误：目录不存在 — {folder}"],
    "s002": ["  文件名：{os.path.basename(file_path)}", "  文件名：{os.path.basename(file_path)}"],
    "s003": ["  后缀名：{os.path.splitext(file_path)[1].lower()}", "  后缀名：{os.path.splitext(file_path)[1].lower()}"],
    "s004": ["  大小：{format_size(stat.st_size)}", "  大小：{format_size(stat.st_size)}"],
    "s005": ["  加入时间：{ctime}", "  加入时间：{ctime}"],
    "s006": ["\n--- {prompt} ---", "\n--- {prompt} ---"],
    "s007": ["  [{i}] {g}", "  [{i}] {g}"],
    "s008": ["  [a] 新增分组", "  [a] 新增分组"],
    "s009": ["✓ 已创建分组：{name}", "✓ 已创建分组：{name}"],
    "s010": ["分组「{group_name}」下没有分类，请先新增。", "分组「{group_name}」下没有分类，请先新增。"],
    "s011": ["✓ 已创建分类：{group_name} → {name}", "✓ 已创建分类：{group_name} → {name}"],
    "s012": ["\n{group_name} 下的分类：", "\n{group_name} 下的分类："],
    "s013": ["  [{i}] {c}  →  {path_hint}", "  [{i}] {c}  →  {path_hint}"],
    "s014": ["  [a] 新增分类", "  [a] 新增分类"],
    "s015": ["\n", "\n"],
    "s016": ["=", "="],
    "s017": ["\n未识别的后缀「{ext}」，请从所有分类中选择：", "\n未识别的后缀「{ext}」，请从所有分类中选择："],
    "s018": ["\n建议分类：{label}  ({cat_path})", "\n建议分类：{label}  ({cat_path})"],
    "s019": ["\n后缀「{ext}」有 {len(ext_mappings)} 个指向：", "\n后缀「{ext}」有 {len(ext_mappings)} 个指向："],
    "s020": ["  [{i}] {g} → {c}  ({cat_path})", "  [{i}] {g} → {c}  ({cat_path})"],
    "s021": ["  [0] 从所有分类中选择", "  [0] 从所有分类中选择"],
    "s022": ["\n分类「{group_name} → {cat_name}」未设置目标路径。", "\n分类「{group_name} → {cat_name}」未设置目标路径。"],
    "s023": ["文件夹名（直接回车默认：{default_name}）: ", "文件夹名（直接回车默认：{default_name}）: "],
    "s024": ["\n✓ 已移动到：{group_name} → {cat_name} → {folder_name}", "\n✓ 已移动到：{group_name} → {cat_name} → {folder_name}"],
    "s025": ["移动失败：{e}", "移动失败：{e}"],
    "s026": ["\n当前没有分组。", "\n当前没有分组。"],
    "s027": ["\n--- 管理分类 ---", "\n--- 管理分类 ---"],
    "s028": ["  [{i}] {g}  ({count} 个分类)", "  [{i}] {g}  ({count} 个分类)"],
    "s029": ["\n分组「{group_name}」下没有分类。", "\n分组「{group_name}」下没有分类。"],
    "s030": ["✓ 已创建分类：{name}", "✓ 已创建分类：{name}"],
    "s031": ["\n{cat_name} ({group_name})", "\n{cat_name} ({group_name})"],
    "s032": ["  路径：{path_display}", "  路径：{path_display}"],
    "s033": ["  [1] 修改路径", "  [1] 修改路径"],
    "s034": ["  [2] 重命名", "  [2] 重命名"],
    "s035": ["  [3] 移动到其他分组", "  [3] 移动到其他分组"],
    "s036": ["  [4] 删除", "  [4] 删除"],
    "s037": ["  [5] 打开目标文件夹", "  [5] 打开目标文件夹"],
    "s038": ["✓ 已重命名为：{new_name}", "✓ 已重命名为：{new_name}"],
    "s039": ["✓ 已移动到分组：{target_group}", "✓ 已移动到分组：{target_group}"],
    "s040": ["\n当前没有后缀映射。", "\n当前没有后缀映射。"],
    "s041": ["\n--- 管理后缀映射 ---", "\n--- 管理后缀映射 ---"],
    "s042": ["  [{i}] {ext}  ({count} 个指向)", "  [{i}] {ext}  ({count} 个指向)"],
    "s043": ["  [a] 新增后缀映射", "  [a] 新增后缀映射"],
    "s044": ["后缀 {ext} 已存在，将添加新的指向。", "后缀 {ext} 已存在，将添加新的指向。"],
    "s045": ["✓ 已添加：{ext} → {g} → {c}", "✓ 已添加：{ext} → {g} → {c}"],
    "s046": ["\n{ext}", "\n{ext}"],
    "s047": ["    [{i}] {g} → {c} {hint}", "    [{i}] {g} → {c} {hint}"],
    "s048": ["  [a] 新增映射", "  [a] 新增映射"],
    "s049": ["  [b] 删除整个后缀", "  [b] 删除整个后缀"],
    "s050": ["\n{g} → {c}", "\n{g} → {c}"],
    "s051": ["  [1] 修改指向", "  [1] 修改指向"],
    "s052": ["  [2] 打开目标文件夹", "  [2] 打开目标文件夹"],
    "s053": ["  [3] 删除此条映射", "  [3] 删除此条映射"],
    "s054": ["✓ 已修改：{ext} → {ng} → {nc}", "✓ 已修改：{ext} → {ng} → {nc}"],
    "s055": ["  [1] 管理分类", "  [1] 管理分类"],
    "s056": ["  [2] 管理后缀映射", "  [2] 管理后缀映射"],
    "s057": ["  [0] 返回主菜单", "  [0] 返回主菜单"],
    "s058": ["    {CONFIG_PATH}", "    {CONFIG_PATH}"],
    "s059": ["    {src_str}", "    {src_str}"],
    "s060": ["  [1] 设置来源目录", "  [1] 设置来源目录"],
    "s061": ["警告：跳过无效路径「{d}」，请使用绝对路径。", "警告：跳过无效路径「{d}」，请使用绝对路径。"],
    "s062": ["  [1] 整理最新下载文件", "  [1] 整理最新下载文件"],
    "s063": ["  [2] 移动指定文件", "  [2] 移动指定文件"],
    "s064": ["  [3] 管理分类配置", "  [3] 管理分类配置"],
    "s065": ["  [4] 设置", "  [4] 设置"],
    "s066": ["  [0] 退出", "  [0] 退出"],

    "    [": ["    [", "    ["],
    "  (": ["  (", "  ("],
    "  [": ["  [", "  ["],
    "  →  ": ["  →  ", "  →  "],
    "  加入时间：": ["  加入时间：", "  加入时间："],
    "  后缀名：": ["  后缀名：", "  后缀名："],
    "  大小：": ["  大小：", "  大小："],
    "  文件名：": ["  文件名：", "  文件名："],
    "  路径：": ["  路径：", "  路径："],
    " (": [" (", " ("],
    " ---": [" ---", " ---"],
    " → ": [" → ", " → "],
    " 下的分类：": [" 下的分类：", " 下的分类："],
    " 个分类)": [" 个分类)", " 个分类)"],
    " 个指向)": [" 个指向)", " 个指向)"],
    " 个指向：": [" 个指向：", " 个指向："],
    " 已存在，将添加新的指向。": [" 已存在，将添加新的指向。", " 已存在，将添加新的指向。"],
    ")": [")", ")"],
    "\n": ["\n", "\n"],
    "\n--- ": ["\n--- ", "\n--- "],
    "\n✓ 已移动到：": ["\n✓ 已移动到：", "\n✓ 已移动到："],
    "\n分类「": ["\n分类「", "\n分类「"],
    "\n分组「": ["\n分组「", "\n分组「"],
    "\n后缀「": ["\n后缀「", "\n后缀「"],
    "\n建议分类：": ["\n建议分类：", "\n建议分类："],
    "\n未识别的后缀「": ["\n未识别的后缀「", "\n未识别的后缀「"],
    "] ": ["] ", "] "],
    "✓ 已修改：": ["✓ 已修改：", "✓ 已修改："],
    "✓ 已创建分类：": ["✓ 已创建分类：", "✓ 已创建分类："],
    "✓ 已创建分组：": ["✓ 已创建分组：", "✓ 已创建分组："],
    "✓ 已添加：": ["✓ 已添加：", "✓ 已添加："],
    "✓ 已移动到分组：": ["✓ 已移动到分组：", "✓ 已移动到分组："],
    "✓ 已重命名为：": ["✓ 已重命名为：", "✓ 已重命名为："],
    "✓ 来源目录已更新：": ["✓ 来源目录已更新：", "✓ 来源目录已更新："],
    "」下没有分类。": ["」下没有分类。", "」下没有分类。"],
    "」下没有分类，请先新增。": ["」下没有分类，请先新增。", "」下没有分类，请先新增。"],
    "」有 ": ["」有 ", "」有 "],
    "」未设置目标路径。": ["」未设置目标路径。", "」未设置目标路径。"],
    "」，请从所有分类中选择：": ["」，请从所有分类中选择：", "」，请从所有分类中选择："],
    "」，请使用绝对路径。": ["」，请使用绝对路径。", "」，请使用绝对路径。"],
    "分组「": ["分组「", "分组「"],
    "后缀 ": ["后缀 ", "后缀 "],
    "文件夹名（直接回车默认：": ["文件夹名（直接回车默认：", "文件夹名（直接回车默认："],
    "移动失败：": ["移动失败：", "移动失败："],
    "警告：跳过无效路径「": ["警告：跳过无效路径「", "警告：跳过无效路径「"],
    "路径不存在：": ["路径不存在：", "路径不存在："],
    "输入无效，请输入 ": ["输入无效，请输入 ", "输入无效，请输入 "],
    "错误：目录不存在 — ": ["错误：目录不存在 — ", "错误：目录不存在 — "],
    "）: ": ["）: ", "）: "],

    "  [2] 切换语言": ["  [2] 切换语言", "  [2] 切换语言"],
    "语言已切换": ["语言已切换", "语言已切换"],
    "输入编号: ": ["输入编号: ", "输入编号: "],

}

def t(key):
    idx = 0 if _current_lang == "zh" else 1
    val = _T.get(key)
    return val[idx] if val else key


BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_PATH = os.path.join(BASE_DIR, "分类配置.json")

DEFAULT_CONFIG = {
    "version": 1,
    "settings": {
        "source_directories": ["D:\\Downloads"],
        "language": "zh"
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
        config["settings"] = {"source_directories": ["D:\\Downloads"],
        "language": "zh"}
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
        print(t("输入无效，请输入 y/n"))


def input_option(prompt: str, valid_options: set) -> str:
    while True:
        val = input(prompt).strip().lower()
        if val in valid_options:
            return val
        print(f"{t("输入无效，请输入 ")}{'/'.join(sorted(valid_options, key=lambda x: (x.isdigit(), x)))}")


def open_folder(path: str):
    if os.path.isdir(path):
        os.startfile(path)
    else:
        print(f"{t("路径不存在：")}{path}")


def get_latest_file(folder: str) -> str | None:
    if not os.path.isdir(folder):
        print(f"{t("错误：目录不存在 — ")}{folder}")
        return None
    entries = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]
    if not entries:
        print(t("目录为空，没有可处理的文件。"))
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
    print(f"{t("  文件名：")}{os.path.basename(file_path)}")
    print(f"{t("  后缀名：")}{os.path.splitext(file_path)[1].lower()}")
    print(f"{t("  大小：")}{format_size(stat.st_size)}")
    print(f"{t("  加入时间：")}{ctime}")


# ========== 分类选择（分组→分类 两级菜单） ==========

def select_classification(cfg: dict, prompt: str = "请选择分类") -> tuple | None:
    """
    返回 (group_name, category_name) 或 None（取消）
    """
    groups = cfg["groups"]

    # --- 选分组 ---
    group_list = list(groups.keys())
    print(f"{t("\n--- ")}{prompt}{t(" ---")}")
    print(t("选择分组："))
    for i, g in enumerate(group_list, 1):
        print(f"{t("  [")}{i}{t("] ")}{g}")
    print(t("  [a] 新增分组"))
    g_valid = {str(i) for i in range(1, len(group_list) + 1)} | {"a", "0"}
    g_choice = input_option("输入编号 (0 取消): ", g_valid)
    if g_choice == "0":
        return None
    if g_choice == "a":
        # 新增分组
        name = input(t("新分组名 (0 取消): ")).strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        if name in groups:
            print(t("该分组已存在。"))
            return None
        groups[name] = {}
        save_config(cfg)
        print(f"{t("✓ 已创建分组：")}{name}")
        group_name = name
    else:
        group_name = group_list[int(g_choice) - 1]

    # --- 选分类 ---
    cat_dict = groups[group_name]
    cat_list = list(cat_dict.keys())
    if not cat_list:
        print(f"{t("分组「")}{group_name}{t("」下没有分类，请先新增。")}")
        # 直接进入新增
        name = input(t("新分类名 (0 取消): ")).strip()
        if not name or name == "0":
            return None
        name = sanitize_folder_name(name)
        path_input = input(t("目标路径（可选，留空后续设置）: ")).strip()
        cat_dict[name] = path_input
        save_config(cfg)
        print(f"{t("✓ 已创建分类：")}{group_name}{t(" → ")}{name}")
        return group_name, name

    print(f"{t("\n")}{group_name}{t(" 下的分类：")}")
    for i, c in enumerate(cat_list, 1):
        path_hint = cat_dict[c] if cat_dict[c] else "（未设置）"
        print(f"{t("  [")}{i}{t("] ")}{c}{t("  →  ")}{path_hint}")
    print(t("  [a] 新增分类"))
    c_valid = {str(i) for i in range(1, len(cat_list) + 1)} | {"a", "0"}
    c_choice = input_option("输入编号 (0 返回): ", c_valid)
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
        print(f"{t("✓ 已创建分类：")}{group_name}{t(" → ")}{name}")
        return group_name, name
    else:
        cat_name = cat_list[int(c_choice) - 1]
        return group_name, cat_name


# ========== 核心整理流程 ==========

def organize_file(file_path: str, cfg: dict):
    if not os.path.isfile(file_path):
        print(t("错误：文件不存在。"))
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
        print(f"{t("\n未识别的后缀「")}{ext}{t("」，请从所有分类中选择：")}")
        target = select_classification(cfg, "从所有分类中选择")
        if target is None:
            return

    elif len(ext_mappings) == 1:
        g, c = ext_mappings[0]
        cat_path = cfg["groups"].get(g, {}).get(c, "")
        label = f"{g} → {c}"
        print(f"{t("\n建议分类：")}{label}{t("  (")}{cat_path}{t(")")}")
        if input_yes_no("是否使用此分类？(y/n): "):
            target = (g, c)
        else:
            target = select_classification(cfg, "请重新选择分类")
            if target is None:
                return

    else:
        print(f"{t("\n后缀「")}{ext}{t("」有 ")}{len(ext_mappings)}{t(" 个指向：")}")
        for i, (g, c) in enumerate(ext_mappings, 1):
            cat_path = cfg["groups"].get(g, {}).get(c, "")
            print(f"{t("  [")}{i}{t("] ")}{g}{t(" → ")}{c}{t("  (")}{cat_path}{t(")")}")
        print(t("  [0] 从所有分类中选择"))
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
        print(f"{t("\n分类「")}{group_name}{t(" → ")}{cat_name}{t("」未设置目标路径。")}")
        set_now = input_yes_no("现在设置？(y/n): ")
        if set_now:
            new_path = input(t("请输入路径: ")).strip()
            if not os.path.isabs(new_path):
                print(t("路径无效，请使用绝对路径。"))
                return
            cfg["groups"][group_name][cat_name] = new_path
            save_config(cfg)
            cat_path = new_path
        else:
            print(t("取消操作。"))
            return

    # 文件夹命名
    default_name = sanitize_folder_name(os.path.splitext(os.path.basename(file_path))[0])
    folder_input = input(f"{t("文件夹名（直接回车默认：")}{default_name}{t("）: ")}").strip()
    folder_name = sanitize_folder_name(folder_input) if folder_input else default_name
    if not folder_name:
        print(t("名称无效，使用默认名。"))
        folder_name = default_name

    target_dir = os.path.join(cat_path, folder_name)

    # 移动
    try:
        os.makedirs(target_dir, exist_ok=True)
        dst = os.path.join(target_dir, os.path.basename(file_path))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(file_path, target_dir)
        print(f"{t("\n✓ 已移动到：")}{group_name}{t(" → ")}{cat_name}{t(" → ")}{folder_name}")
    except Exception as e:
        print(f"{t("移动失败：")}{e}")
        return

    if input_yes_no("是否打开目标文件夹？(y/n): "):
        open_folder(target_dir)


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
            print(f"{t("✓ 已创建分组：")}{name}")
            continue

        print(t("\n--- 管理分类 ---"))
        print(t("现有分组："))
        for i, g in enumerate(group_list, 1):
            count = len(groups[g])
            print(f"{t("  [")}{i}{t("] ")}{g}{t("  (")}{count}{t(" 个分类)")}")
        print(t("  [a] 新增分组"))
        g_valid = {str(i) for i in range(1, len(group_list) + 1)} | {"a", "0"}
        g_choice = input_option("输入编号 (0 返回): ", g_valid)
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
            print(f"{t("✓ 已创建分组：")}{name}")
            continue

        group_name = group_list[int(g_choice) - 1]
        cat_dict = groups[group_name]
        cat_list = list(cat_dict.keys())

        while True:
            if not cat_list:
                print(f"{t("\n分组「")}{group_name}{t("」下没有分类。")}")
                name = input(t("新分类名 (0 返回分组列表): ")).strip()
                if not name or name == "0":
                    break
                name = sanitize_folder_name(name)
                path_input = input(t("目标路径（可选）: ")).strip()
                cat_dict[name] = path_input
                save_config(cfg)
                print(f"{t("✓ 已创建分类：")}{name}")
                cat_list = list(cat_dict.keys())
                if not cat_list:
                    break
                continue

            print(f"{t("\n")}{group_name}{t(" 下的分类：")}")
            for i, c in enumerate(cat_list, 1):
                path_hint = cat_dict[c] if cat_dict[c] else "（未设置）"
                print(f"{t("  [")}{i}{t("] ")}{c}{t("  →  ")}{path_hint}")
            print(t("  [a] 新增分类"))
            c_valid = {str(i) for i in range(1, len(cat_list) + 1)} | {"a", "0"}
            c_choice = input_option("输入编号 (0 返回分组列表): ", c_valid)
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
                print(f"{t("✓ 已创建分类：")}{name}")
                cat_list = list(cat_dict.keys())
                continue

            cat_name = cat_list[int(c_choice) - 1]
            current_path = cat_dict[cat_name]

            # --- 分类操作菜单 ---
            while True:
                path_display = current_path if current_path else "（未设置）"
                print(f"{t("\n")}{cat_name}{t(" (")}{group_name}{t(")")}")
                print(f"{t("  路径：")}{path_display}")
                print()
                print(t("  [1] 修改路径"))
                print(t("  [2] 重命名"))
                print(t("  [3] 移动到其他分组"))
                print(t("  [4] 删除"))
                print(t("  [5] 打开目标文件夹"))
                act_valid = {"1", "2", "3", "4", "5", "0"}
                act = input_option("输入编号 (0 取消): ", act_valid)

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
                    print(t("✓ 路径已更新。"))

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
                    # 更新此分类在 extensions 里的引用
                    cat_dict[new_name] = cat_dict.pop(cat_name)
                    for ext, mappings in cfg["extensions"].items():
                        for i, (g, c) in enumerate(mappings):
                            if g == group_name and c == cat_name:
                                mappings[i][1] = new_name
                    save_config(cfg)
                    print(f"{t("✓ 已重命名为：")}{new_name}")
                    cat_name = new_name
                    cat_list = list(cat_dict.keys())

                elif act == "3":
                    other_groups = [g for g in groups if g != group_name]
                    if not other_groups:
                        print(t("没有其他分组可移动。"))
                        continue
                    print(t("目标分组："))
                    for i, g in enumerate(other_groups, 1):
                        print(f"{t("  [")}{i}{t("] ")}{g}")
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
                    print(f"{t("✓ 已移动到分组：")}{target_group}")
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
                        print(t("✓ 已删除。"))
                        cat_list = list(cat_dict.keys())
                        break  # 返回分类列表

                elif act == "5":
                    if current_path:
                        open_folder(current_path)
                    else:
                        print(t("未设置路径。"))


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
                print(f"{t("  [")}{i}{t("] ")}{ext}{t("  (")}{count}{t(" 个指向)")}")

        print(t("  [a] 新增后缀映射"))
        e_valid = {str(i) for i in range(1, len(ext_list) + 1)} | {"a", "0"}
        e_choice = input_option("输入编号 (0 返回): ", e_valid)
        if e_choice == "0":
            return

        # --- 新增后缀 ---
        if e_choice == "a":
            ext = input(t("请输入后缀名（如 .png，0 取消）: ")).strip().lower()
            if ext == "0" or not ext:
                continue
            if not ext.startswith("."):
                ext = "." + ext

            if ext in ext_dict:
                print(f"{t("后缀 ")}{ext}{t(" 已存在，将添加新的指向。")}")

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
                print(f"{t("✓ 已添加：")}{ext}{t(" → ")}{g}{t(" → ")}{c}")
                if not input_yes_no("是否继续添加指向？(y/n): "):
                    break
            continue

        # --- 选择后缀 ---
        ext = ext_list[int(e_choice) - 1]
        mappings = ext_dict[ext]

        while True:
            print(f"{t("\n")}{ext}")
            print(t("  现有映射："))
            for i, (g, c) in enumerate(mappings, 1):
                cat_path = cfg["groups"].get(g, {}).get(c, "")
                hint = f"  ({cat_path})" if cat_path else ""
                print(f"{t("    [")}{i}{t("] ")}{g}{t(" → ")}{c} {hint}")
            print()
            print(t("  [a] 新增映射"))
            print(t("  [b] 删除整个后缀"))

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
                print(f"{t("✓ 已添加：")}{ext}{t(" → ")}{g}{t(" → ")}{c}")
                continue

            if m_choice == "b":
                if input_yes_no(f"确认删除后缀 {ext} 的所有映射？(y/n): "):
                    del ext_dict[ext]
                    save_config(cfg)
                    print(t("✓ 已删除。"))
                    break
                continue

            # --- 选中单条映射的操作 ---
            g, c = mappings[int(m_choice) - 1]
            cat_path = cfg["groups"].get(g, {}).get(c, "")

            while True:
                path_display = cat_path if cat_path else "（未设置）"
                print(f"{t("\n")}{g}{t(" → ")}{c}")
                print(f"{t("  路径：")}{path_display}")
                print()
                print(t("  [1] 修改指向"))
                print(t("  [2] 打开目标文件夹"))
                print(t("  [3] 删除此条映射"))
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
                    print(f"{t("✓ 已修改：")}{ext}{t(" → ")}{ng}{t(" → ")}{nc}")
                    g, c = ng, nc
                    cat_path = cfg["groups"].get(g, {}).get(c, "")

                elif m_act == "2":
                    if cat_path:
                        open_folder(cat_path)
                    else:
                        print(t("未设置路径。"))

                elif m_act == "3":
                    if input_yes_no("确认删除此条映射？(y/n): "):
                        mappings.pop(int(m_choice) - 1)
                        if not mappings:
                            del ext_dict[ext]
                        save_config(cfg)
                        print(t("✓ 已删除。"))
                        break  # 回到后缀详情


# ========== 配置管理主菜单 ==========

def manage_config(cfg: dict):
    while True:
        print("\n" + "=" * 48)
        print(t("  配置管理"))
        print("=" * 48)
        print(t("  [1] 管理分类"))
        print(t("  [2] 管理后缀映射"))
        print(t("  [0] 返回主菜单"))
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
        print(t("  设置"))
        print("=" * 48)
        print(t("  配置文件路径："))
        print(f"    {CONFIG_PATH}")
        print()
        src_dirs = cfg.get("settings", {}).get("source_directories", ["D:\\Downloads"])
        src_str = "、".join(src_dirs) if src_dirs else "（未设置）"
        print(t("  来源目录："))
        print(f"    {src_str}")
        print()
        print(t("  [1] 设置来源目录"))
        print(t("  [2] 切换语言"))
        print(t("  [0] 返回主菜单"))
        choice = input_option(t("输入编号: "), {"1", "2", "0"})
        if choice == "0":
            return
        if choice == "1":
            new_dir = input(t("请输入来源目录路径 (多个用逗号分隔，0 取消): ")).strip()
            if new_dir == "0" or not new_dir:
                continue
            dirs = [d.strip() for d in new_dir.split(",") if d.strip()]
            valid_dirs = []
            for d in dirs:
                if os.path.isabs(d):
                    valid_dirs.append(d)
                else:
                    print(f"{t("警告：跳过无效路径「")}{d}{t("」，请使用绝对路径。")}")
            if valid_dirs:
                cfg["settings"]["source_directories"] = valid_dirs
                save_config(cfg)
                print(f"{t("✓ 来源目录已更新：")}{'、'.join(valid_dirs)}")
            else:
                print(t("未设置有效的目录。"))

        elif choice == "2":
            global _current_lang
            lang = "en" if _current_lang == "zh" else "zh"
            _current_lang = lang
            cfg["settings"]["language"] = lang
            save_config(cfg)
            print(t("语言已切换"))


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
        print(t("  文件归档工具"))
        print("=" * 48)
        print(t("  [1] 整理最新下载文件"))
        print(t("  [2] 移动指定文件"))
        print(t("  [3] 管理分类配置"))
        print(t("  [4] 设置"))
        print(t("  [0] 退出"))
        choice = input_option("输入编号: ", {"1", "2", "3", "4", "0"})

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
            path = input(t("请输入文件路径 (0 取消): ")).strip()
            if path == "0":
                continue
            if not os.path.isfile(path):
                print(t("错误：文件不存在。"))
                continue
            organize_file(path, cfg)

        elif choice == "3":
            manage_config(cfg)

        elif choice == "4":
            manage_settings(cfg)

if __name__ == "__main__":
    main()
