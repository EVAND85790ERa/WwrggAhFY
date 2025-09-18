# 代码生成时间: 2025-09-18 12:16:52
import os
import shutil
from quart import Quart, jsonify, request, abort

# 创建一个Quart应用
app = Quart(__name__)

# 定义一个函数，用于整理文件夹内文件结构
def organize_folder_structure(source_folder, dest_folder):
    """
    将源文件夹中的文件移动到目标文件夹，并按照文件类型进行分类。

    Args:
    source_folder (str): 源文件夹路径。
    dest_folder (str): 目标文件夹路径。

    Returns:
    dict: 包含操作结果的字典。
    """
    try:
        # 检查源文件夹和目标文件夹是否存在
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"源文件夹 '{source_folder}' 不存在。")
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # 获取源文件夹中的所有文件
        files = os.listdir(source_folder)
        for file in files:
            file_path = os.path.join(source_folder, file)
            # 检查是否为文件
            if os.path.isfile(file_path):
                # 获取文件扩展名
                _, ext = os.path.splitext(file)
                # 定义目标文件夹路径
                target_folder_path = os.path.join(dest_folder, ext.lstrip('.'))
                # 如果目标文件夹不存在，则创建
                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                # 移动文件到目标文件夹
                shutil.move(file_path, target_folder_path)

        return {"status": "success", "message": "文件夹整理完成。"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 创建一个路由，用于处理文件夹整理请求
@app.route('/organize', methods=['POST'])
async def organize():
    """
    处理文件夹整理请求。
    """
    try:
        # 获取请求数据
        data = await request.get_json()
        source_folder = data.get('source_folder')
        dest_folder = data.get('dest_folder')

        # 检查请求数据是否完整
        if not source_folder or not dest_folder:
            abort(400, description="请求数据不完整。")

        # 调用整理函数
        result = organize_folder_structure(source_folder, dest_folder)

        # 返回结果
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

# 运行Quart应用
if __name__ == '__main__':
    app.run(debug=True)