# 代码生成时间: 2025-08-19 09:39:16
import os
import re
from quart import Quart, request, jsonify

# 创建 Quart 应用
app = Quart(__name__)

# 定义一个正则表达式模式用于匹配和查找文件名
file_pattern = re.compile(r"^(.*)\((\d+)\)\.(.*)$")

# 批量重命名文件的函数
def batch_rename(directory, new_pattern):
    try:
        # 获取目录中的所有文件
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # 对每个文件进行重命名操作
        for file in files:
            match = file_pattern.match(file)
            if match:
                # 构建新文件名
                base, number, extension = match.groups()
                new_name = f"{new_pattern.format(**match.groupdict())}.{extension}"
                old_path = os.path.join(directory, file)
                new_path = os.path.join(directory, new_name)

                # 重命名文件
                os.rename(old_path, new_path)
                print(f"Renamed '{file}' to '{new_name}'")
            else:
                print(f"Skipped '{file}' as it does not match the pattern.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 提供一个 API 接口来处理批量重命名请求
@app.route('/rename', methods=['POST'])
async def rename_files():
    try:
        # 获取请求参数
        data = await request.get_json()
        directory = data['directory']
        new_pattern = data['new_pattern']

        # 执行批量重命名
        batch_rename(directory, new_pattern)

        # 返回成功响应
        return jsonify({'message': 'Files have been renamed successfully'})
    except Exception as e:
        # 返回错误响应
        return jsonify({'error': str(e)}), 400

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)