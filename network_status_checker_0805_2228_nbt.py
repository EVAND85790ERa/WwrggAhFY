# 代码生成时间: 2025-08-05 22:28:46
# network_status_checker.py

"""
网络连接状态检查器
使用Quart框架创建一个简单的网络连接状态检查器
"""

from quart import Quart, request, jsonify, abort
import requests
import socket
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

app = Quart(__name__)

# 检查网络连接状态的函数
def check_network_connection(host='8.8.8.8', port=53):
    """
    检查网络连接状态
    :param host: 要检查的主机，默认为Google DNS服务器
    :param port: 要检查的端口，默认为53（DNS）
    :return: True如果连接成功，否则False
    """
    try:
        socket.create_connection((host, port), 2)  # 尝试连接
        return True
    except OSError:
        return False

@app.before_serving
async def configure_logging():
    """
    配置日志记录器
    """
    app.logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

@app.route('/check', methods=['GET'])
async def check_connection():
    """
    检查网络连接状态的端点
    """
    host = request.args.get('host', '8.8.8.8')  # 默认检查Google DNS服务器
    port = request.args.get('port', 53, type=int)  # 默认检查端口53
    connected = check_network_connection(host, port)
    if connected:
        return jsonify({'status': 'connected'})
    else:
        return jsonify({'status': 'disconnected'})

@app.errorhandler(404)
async def not_found(error):
    """
    处理404错误
    """
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
async def internal_server_error(error):
    """
    处理500错误
    """
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)  # 启动Quart服务器