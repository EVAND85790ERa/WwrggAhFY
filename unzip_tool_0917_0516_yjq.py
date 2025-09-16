# 代码生成时间: 2025-09-17 05:16:15
import quart
from zipfile import ZipFile
from pathlib import Path
import os

# 确定静态文件目录
STATIC_FOLDER = 'static'

app = quart.Quart(__name__)

"""
压缩文件解压工具

这个应用程序使用QUART框架实现一个简单的压缩文件解压工具。
用户可以通过POST请求上传ZIP文件，应用程序将解压文件到指定目录。
"""

@app.route('/upload', methods=['POST'])
async def upload_zip_file():
    """
    处理上传的ZIP文件并解压
    
    返回：
        - 如果成功，返回解压后的文件列表
        - 如果失败，返回错误信息
    """
    # 获取上传的文件
    file = await quart.request.files['file']
    if not file:
        return {'error': 'No file uploaded'}, 400

    # 创建ZIP文件路径
    zip_path = os.path.join(STATIC_FOLDER, file.filename)
    file_path = await file.save(zip_path)

    # 检查文件是否已存在
    if not file_path:
        return {'error': 'Failed to save file'}, 500

    try:
        # 解压文件
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(STATIC_FOLDER)

        # 获取解压后的文件列表
        extracted_files = [file for file in os.listdir(STATIC_FOLDER) if file != file.filename]
        return {'files': extracted_files}
    except Exception as e:
        # 处理解压过程中的错误
        return {'error': str(e)}, 500
    finally:
        # 删除临时ZIP文件
        os.remove(zip_path)

if __name__ == '__main__':
    app.run(debug=True)