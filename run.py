#!/usr/bin/env python3
"""入口：将 app/ 加入路径后启动程序"""
import os
import sys


if not getattr(sys, "frozen", False):
    # 开发模式：指向源码 app/ 目录
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
    sys.path.insert(0, app_dir)
    os.chdir(app_dir)

from main import main

main()
