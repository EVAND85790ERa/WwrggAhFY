# 代码生成时间: 2025-08-09 17:33:36
# config_manager.py

from quart import Quart, jsonify
import json
import os

# 创建 Quart 应用
app = Quart(__name__)

# 存储配置文件的路径
CONFIG_PATH = 'config.json'

# 检查配置文件是否存在，如果不存在则创建一个空的配置文件
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump({}, config_file)


@app.route('/config', methods=['GET', 'POST'])
async def config():
    """
    配置文件管理器的接口，允许获取和更新配置。
    GET 请求会返回当前的配置。
    POST 请求可以更新配置文件。
    """
    if request.method == 'GET':
        try:
            with open(CONFIG_PATH, 'r') as config_file:
                config_data = json.load(config_file)
                return jsonify(config_data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON in config file'}), 500
        except IOError:
            return jsonify({'error': 'Config file not found'}), 404
    elif request.method == 'POST':
        try:
            data = await request.get_json()
            with open(CONFIG_PATH, 'w') as config_file:
                json.dump(data, config_file, indent=4)
            return jsonify({'message': 'Config updated successfully'}), 200
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON in request body'}), 400
        except IOError:
            return jsonify({'error': 'Failed to write to config file'}), 500

if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)