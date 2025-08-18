# 代码生成时间: 2025-08-18 17:50:24
# process_manager.py

# 导入Quart框架和psutil库
from quart import Quart, jsonify, request
import psutil

# 创建Quart应用
app = Quart(__name__)

# 定义一个路由，用于获取所有进程信息
@app.route('/processes', methods=['GET'])
async def get_processes():
    try:
        # 获取所有进程信息
        processes = psutil.process_iter(['pid', 'name', 'status', 'create_time'])
        # 将进程信息转换为字典列表
        process_list = [{'pid': proc.info['pid'], 'name': proc.info['name'], 'status': proc.info['status'], 'create_time': proc.info['create_time']} for proc in processes]
        return jsonify(process_list)
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500

# 定义一个路由，用于启动一个新进程
@app.route('/start', methods=['POST'])
async def start_process():
    try:
        # 获取请求体中的进程名称和命令行参数
        data = await request.get_json()
        process_name = data['process_name']
        cmd_line = data['cmd_line']
        # 使用psutil启动进程
        process = psutil.Popen(cmd_line, creationflags=psutil.CREATE_NEW_PROCESS_GROUP)
        # 返回新进程的信息
        return jsonify({'pid': process.pid, 'name': process_name})
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500

# 定义一个路由，用于终止一个进程
@app.route('/stop', methods=['POST'])
async def stop_process():
    try:
        # 获取请求体中的进程ID
        data = await request.get_json()
        pid = data['pid']
        # 使用psutil终止进程
        process = psutil.Process(pid)
        process.terminate()
        process.wait()
        # 返回成功响应
        return jsonify({'message': f'Process {pid} terminated successfully'})
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500

# 运行Quart应用
if __name__ == '__main__':
    app.run()
