# 代码生成时间: 2025-09-22 03:24:35
import numpy as np
from quart import Quart, jsonify, request

"""
数据生成器程序，用于生成随机测试数据。
支持生成随机整数、浮点数和字符串数据。
"""

app = Quart(__name__)

# 定义路由和相应的处理函数
@app.route('/generate', methods=['POST'])
async def generate_data():
    # 获取请求数据
    data = await request.get_json()
    
    # 验证数据格式
    if not data or 'type' not in data or 'count' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # 根据请求类型生成数据
# 增强安全性
    if data['type'] == 'int':
        return jsonify({'data': [np.random.randint(0, 100) for _ in range(data['count'])]})
    elif data['type'] == 'float':
        return jsonify({'data': [np.random.random() for _ in range(data['count'])]})
    elif data['type'] == 'string':
        return jsonify({'data': [''.join(np.random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) for _ in range(data['count'])]})
# FIXME: 处理边界情况
    else:
        return jsonify({'error': 'Unsupported data type'}), 400
# NOTE: 重要实现细节

# 错误处理
@app.errorhandler(404)
async def not_found(error):
    return jsonify({'error': 'Not found'}), 404
# 改进用户体验

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
