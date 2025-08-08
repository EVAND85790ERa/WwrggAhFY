# 代码生成时间: 2025-08-09 04:44:35
import os
import shutil
from quart import Quart, jsonify

# 定义一个Quart应用
app = Quart(__name__)


@app.route('/api/backup', methods=['POST'])
async def backup_file():
    # 获取请求中的文件路径参数
    file_path = request.form.get('file_path')
    backup_path = request.form.get('backup_path')

    # 检查文件路径和备份路径是否有效
    if not file_path or not backup_path:
        return jsonify(error='Missing file_path or backup_path'), 400
    if not os.path.exists(file_path):
        return jsonify(error='File not found'), 404

    try:
        # 备份文件
        shutil.copy2(file_path, backup_path)
        return jsonify(message='File backed up successfully', file_path=file_path, backup_path=backup_path), 200
    except Exception as e:
        # 处理备份过程中的异常
        return jsonify(error=str(e)), 500


@app.route('/api/sync', methods=['POST'])
async def sync_files():
    # 获取请求中的源路径和目标路径参数
    source_path = request.form.get('source_path')
    target_path = request.form.get('target_path')

    # 检查源路径和目标路径是否有效
    if not source_path or not target_path:
        return jsonify(error='Missing source_path or target_path'), 400
    if not os.path.exists(source_path):
        return jsonify(error='Source path not found'), 404

    try:
        # 同步文件
        shutil.copytree(source_path, target_path)
        return jsonify(message='Files synced successfully', source_path=source_path, target_path=target_path), 200
    except Exception as e:
        # 处理同步过程中的异常
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
