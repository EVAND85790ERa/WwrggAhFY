# 代码生成时间: 2025-08-10 03:09:56
import json
from quart import Quart, jsonify, request

# 创建Quart应用
app = Quart(__name__)

class ConfigManager:
    """配置文件管理器类"""
    def __init__(self):
        self.configs = {}

    def load(self, file_path):
        """从文件加载配置"""
        try:
            with open(file_path, 'r') as f:
                self.configs = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {file_path} 未找到")
        except json.JSONDecodeError:
            raise ValueError(f"配置文件 {file_path} 格式错误")

    def get(self, key):
        """获取配置项"""
        return self.configs.get(key)

    def set(self, key, value):
        """设置配置项"""
        self.configs[key] = value

    def save(self, file_path):
        """保存配置到文件"""
        with open(file_path, 'w') as f:
            json.dump(self.configs, f, indent=4)

@app.route('/config', methods=['GET', 'POST'])
async def config_route():
    """配置接口"""
    manager = ConfigManager()
    if request.method == 'POST':
        data = await request.get_json()
        manager.set(data['key'], data['value'])
        manager.save('config.json')
        return jsonify({'message': '配置更新成功'})
    elif request.method == 'GET':
        config_key = request.args.get('key')
        if config_key:
            config_value = manager.get(config_key)
            if config_value is None:
                return jsonify({'error': '配置项未找到'})
            return jsonify({'key': config_key, 'value': config_value})
        return jsonify(manager.configs)

if __name__ == '__main__':
    app.run()
