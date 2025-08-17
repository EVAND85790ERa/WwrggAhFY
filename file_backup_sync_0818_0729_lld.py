# 代码生成时间: 2025-08-18 07:29:50
import os
import shutil
from quart import Quart, jsonify

# 创建一个Quart应用
app = Quart(__name__)

# 定义备份和同步文件的函数
def backup_and_sync(source_path, backup_path):
    """备份源路径的文件到备份路径，如果文件已存在则同步更新。"""
    try:
        # 创建备份路径如果它不存在
        os.makedirs(backup_path, exist_ok=True)
        
        # 遍历源路径中的所有文件
        for item in os.listdir(source_path):
            source_item_path = os.path.join(source_path, item)
            backup_item_path = os.path.join(backup_path, item)
            
            # 如果是文件夹，则递归同步
            if os.path.isdir(source_item_path):
                backup_and_sync(source_item_path, backup_item_path)
            # 如果是文件，则复制文件
            elif os.path.isfile(source_item_path):
                shutil.copy2(source_item_path, backup_item_path)
        return {'status': 'success', 'message': 'Backup and sync completed successfully.'}
    except Exception as e:
        # 处理异常
        return {'status': 'error', 'message': str(e)}

# 定义路由和对应的处理函数
@app.route('/backup_sync', methods=['POST'])
async def backup_sync():
    # 从请求中获取源路径和备份路径
    data = await request.get_json()
    source_path = data.get('source_path')
    backup_path = data.get('backup_path')
    
    # 检查路径是否提供
    if not source_path or not backup_path:
        return jsonify({'status': 'error', 'message': 'Source and backup paths are required.'})
    
    # 调用备份和同步函数
    result = backup_and_sync(source_path, backup_path)
    return jsonify(result)

# 运行Quart应用
if __name__ == '__main__':
    app.run(debug=True)