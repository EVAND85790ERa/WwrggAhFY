# 代码生成时间: 2025-08-07 15:16:07
import os
import shutil
from quart import Quart, jsonify, request

# 创建一个Quart应用
app = Quart(__name__)

# 定义文件夹结构整理器类
class FolderOrganizer:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        # 确保源文件夹存在
        if not os.path.exists(self.source_folder):
            raise ValueError(f"源文件夹{self.source_folder}不存在")

    def organize(self):
        "