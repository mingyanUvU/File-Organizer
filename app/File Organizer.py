#!/usr/bin/env python3
"""入口文件"""
import os
import sys

if not getattr(sys, "frozen", False):
    os.environ["FILE_ORGANIZER_ENTRY"] = os.path.abspath(__file__)

from main import main

if __name__ == "__main__":
    main()
