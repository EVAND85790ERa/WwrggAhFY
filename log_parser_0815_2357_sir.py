# 代码生成时间: 2025-08-15 23:57:31
import quart
from quart import jsonify
import re
import json
from datetime import datetime

# 定义日志文件解析工具的主要功能
class LogParser:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s-\s(INFO|ERROR|WARN|DEBUG)\s-\s(.*)"

    # 解析日志文件
    def parse_log_file(self):
        try:
            with open(self.log_file_path, 'r') as file:
                logs = []
                for line in file:
                    match = re.match(self.pattern, line)
                    if match:
                        timestamp, level, message = match.groups()
                        log_entry = {
                            'timestamp': timestamp,
                            'level': level,
                            'message': message.strip()
                        }
                        logs.append(log_entry)
                return logs
        except FileNotFoundError:
            raise ValueError(f'Log file not found at {self.log_file_path}')
        except Exception as e:
            raise ValueError(f'An error occurred: {str(e)}')

# 创建Quart应用
app = quart.Quart(__name__)

# 定义API端点，用于解析日志文件
@app.route('/api/parse-logs', methods=['POST'])
async def parse_logs():
    data = await quart.request.get_json()
    log_file_path = data.get('log_file_path')

    if not log_file_path:
        return jsonify({'error': 'Log file path is required'}), 400

    try:
# 改进用户体验
        parser = LogParser(log_file_path)
        logs = parser.parse_log_file()
        return jsonify(logs)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
# 添加错误处理

# 启动Quart应用
if __name__ == '__main__':
    app.run(debug=True)