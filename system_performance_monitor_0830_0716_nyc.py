# 代码生成时间: 2025-08-30 07:16:49
from quart import Quart, jsonify
import psutil
import platform

"""
系统性能监控工具
"""
app = Quart(__name__)

@app.route('/performance', methods=['GET'])
def get_system_performance():
    """
    获取系统性能信息
    
    Returns:
        dict: 包含系统性能信息的字典
    """
    try:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        # 获取内存使用情况
        memory = psutil.virtual_memory()
        # 获取磁盘使用情况
        disk = psutil.disk_usage('/')
        # 获取网络信息
        net_io = psutil.net_io_counters()
        # 获取系统信息
        system_info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version()
        }
        # 组织性能数据
        performance_data = {
            'cpu_usage': cpu_usage,
            'memory_usage': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            },
            'disk_usage': {
                'total': disk.total,
                'available': disk.free,
                'used': disk.used,
                'percent': disk.percent
            },
            'network_io': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv
            },
            'system_info': system_info
        }
        return jsonify(performance_data)
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 运行应用
    app.run(host='0.0.0.0', port=5000)