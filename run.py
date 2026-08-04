#!/usr/bin/env python3
"""入口：将 app/ 加入路径后启动程序"""
import os
import sys


if not getattr(sys, "frozen", False):
    # 开发模式：指向源码 app/ 目录
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
    # 记录入口脚本绝对路径，供恢复出厂设置后重启使用
    os.environ["FILE_ORGANIZER_ENTRY"] = os.path.abspath(__file__)
    sys.path.insert(0, app_dir)
    os.chdir(app_dir)

from main import main

main()
