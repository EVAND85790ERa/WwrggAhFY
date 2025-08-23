# 代码生成时间: 2025-08-23 17:22:59
import os
import shutil
from quart import Quart, jsonify, request
from werkzeug.exceptions import BadRequest

# 初始化Quart应用
app = Quart(__name__)

class DataBackupRestoreService:
    """数据备份和恢复服务类"""
    def __init__(self, backup_dir, data_dir):
        self.backup_dir = backup_dir
        self.data_dir = data_dir
        self.backup_path = os.path.join(self.backup_dir, "backup")

    def backup_data(self):
        "