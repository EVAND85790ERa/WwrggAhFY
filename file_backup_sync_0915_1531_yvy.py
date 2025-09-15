# 代码生成时间: 2025-09-15 15:31:59
import os
import shutil
import logging
from quart import Quart, jsonify, request, abort

# 设置日志记录
logging.basicConfig(level=logging.INFO)

app = Quart(__name__)

# 定义配置变量
BACKUP_DIR = "backup/"
SOURCE_DIR = "source/"

# 确保备份目录存在
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# 备份文件
def backup_file(source_path):
    try:
        # 获取文件名
        filename = os.path.basename(source_path)
        backup_path = os.path.join(BACKUP_DIR, filename)
        # 执行备份操作
        shutil.copy2(source_path, backup_path)
        return True
    except Exception as e:
        logging.error(f"Error backing up file: {e}")
        return False

# 同步文件
def sync_files(source_path, target_path):
    try:
        # 确保目标目录存在
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        # 递归同步两个目录
        for item in os.listdir(source_path):
            source_item = os.path.join(source_path, item)
            target_item = os.path.join(target_path, item)
            if os.path.isdir(source_item):
                sync_files(source_item, target_item)
            else:
                shutil.copy2(source_item, target_item)
        return True
    except Exception as e:
        logging.error(f"Error syncing files: {e}")
        return False

# API端点：备份单个文件
@app.route("/backup", methods=["POST"])
async def backup_file_api():
    file = await request.files.get("file")
    if not file:
        abort(400, description="No file part")
    source_path = os.path.join(SOURCE_DIR, file.filename)
    file.save(source_path)
    if backup_file(source_path):
        return jsonify(success=True, message="File backed up successfully")
    else:
        return jsonify(success=False, message="Failed to backup file")

# API端点：同步目录
@app.route("/sync", methods=["POST"])
async def sync_directory_api():
    data = await request.get_json()
    source_path = data.get("source")
    target_path = data.get("target")
    if not source_path or not target_path:
        abort(400, description="Missing source or target path")
    if not os.path.exists(source_path):
        abort(404, description="Source path does not exist")
    if not os.path.exists(target_path):
        abort(404, description="Target path does not exist")
    if sync_files(source_path, target_path):
        return jsonify(success=True, message="Directory synced successfully")
    else:
        return jsonify(success=False, message="Failed to sync directory")

if __name__ == '__main__':
    app.run(debug=True)