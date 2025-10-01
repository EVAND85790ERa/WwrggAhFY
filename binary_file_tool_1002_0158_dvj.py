# 代码生成时间: 2025-10-02 01:58:28
import quart
from quart import request, jsonify
import os

# 二进制文件读写工具应用
app = quart.Quart(__name__)

"""
该函数用于读取二进制文件并返回其内容。
:param file_path: 要读取的二进制文件的路径
:return: 文件内容的字节流
"""
@app.route('/read', methods=['POST'])
def read_binary_file():
    data = request.json
    file_path = data.get('file_path')
    if not file_path:
        return jsonify({'error': 'Missing file_path parameter'}), 400
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
        return jsonify({'file_content': file_content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
该函数用于将二进制内容写入文件。
:param file_path: 要写入的文件的路径
:param file_content: 要写入的二进制内容
:return: 写入结果
"""
@app.route('/write', methods=['POST'])
def write_binary_file():
    data = request.json
    file_path = data.get('file_path')
    file_content = data.get('file_content')
    if not file_path or not file_content:
        return jsonify({'error': 'Missing file_path or file_content parameter'}), 400
    try:
        with open(file_path, 'wb') as file:
            file.write(file_content)
        return jsonify({'message': 'File written successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)