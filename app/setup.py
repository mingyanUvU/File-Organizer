import os
from config import save_config
from i18n import t, set_language
from utils import input_yes_no


def first_run_setup(cfg: dict):
    """首次运行引导：语言选择 + 基本提示"""
    print("=" * 48)
    print("  File Organizer")
    print("=" * 48)
    print()
    print("  Welcome! / 欢迎使用！")
    print()
    print("  请选择语言 / Select language:")
    print("    [1] \u4e2d\u6587")   # 中文
    print("    [2] English")

    choice = input("  \u8f93\u5165\u7f16\u53f7 / Enter number: ").strip()  # 输入编号
    lang = "zh" if choice != "2" else "en"

    set_language(lang)
    cfg["settings"]["language"] = lang
    save_config(cfg)

    print(f"  {t('语言已切换') if lang == 'en' else t('语言已切换')}")
    print()
    _home = os.path.expanduser("~")
    print(f"  {t('配置已包含')} Windows\u7cfb\u7edf\u9ed8\u8ba4 {t('分组')}:")
    print(f"    {t('文档')} \u2192 {os.path.join(_home, 'Documents')}")
    print(f"    {t('图片')} \u2192 {os.path.join(_home, 'Pictures')}")
    print(f"    {t('视频')} \u2192 {os.path.join(_home, 'Videos')}")
    print(f"    {t('音乐')} \u2192 {os.path.join(_home, 'Music')}")
    print()
    print(f"  {t('你可以直接整理文件，或到管理分类配置新增分组。')}")
    print()

    while True:
        inp = input(f"  {t('是否现在设置来源目录？')}(y/n): ").strip().lower()
        if inp in ("y", "yes", "\u662f"):  # 是
            from settings import manage_settings
            manage_settings(cfg)
            return
        if inp in ("n", "no", "\u5426"):  # 否
            print(f"  {t('跳过，退出程序。')}")
            return
        print(f"  {t('输入无效，请输入 y/n')}")
