#!/usr/bin/env python3
"""入口：将 app/ 加入路径后启动程序"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))
os.chdir(os.path.join(os.path.dirname(__file__), "app"))
from main import main

main()
