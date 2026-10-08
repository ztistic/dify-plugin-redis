import os
import sys

# 将项目根目录加入 sys.path，使测试能导入 tools / utils 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
