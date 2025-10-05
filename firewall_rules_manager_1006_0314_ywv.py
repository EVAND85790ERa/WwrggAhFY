# 代码生成时间: 2025-10-06 03:14:21
import quart
from quart import request, jsonify
from typing import Dict

# 定义防火墙规则存储结构
firewall_rules = {
    'rules': []
}

# 创建一个Quart应用程序
app = quart.Quart(__name__)

# 定义添加防火墙规则的路由
@app.route('/add_rule', methods=['POST'])
async def add_firewall_rule():
    try:
        # 获取请求体中的数据
        data = await request.get_json()
        
        # 检查请求体中是否包含规则信息
        if 'rule' not in data:
            return jsonify({'error': 'Missing rule information'}), 400
        
        # 将新规则添加到防火墙规则列表中
        firewall_rules['rules'].append(data['rule'])
        
        # 返回成功响应
        return jsonify({'message': 'Rule added successfully'}), 201
    
    except Exception as e:
        # 返回错误响应
        return jsonify({'error': str(e)}), 500

# 定义获取所有防火墙规则的路由
@app.route('/rules', methods=['GET'])
async def get_firewall_rules():
    try:
        # 返回所有防火墙规则
        return jsonify(firewall_rules), 200
    
    except Exception as e:
        # 返回错误响应
        return jsonify({'error': str(e)}), 500

# 定义删除防火墙规则的路由
@app.route('/delete_rule/<rule_id>', methods=['DELETE'])
async def delete_firewall_rule(rule_id: int):
    try:
        # 查找要删除的规则
        rule_to_delete = next((rule for rule in firewall_rules['rules'] if rule['id'] == rule_id), None)
        
        # 如果规则不存在，返回错误响应
        if not rule_to_delete:
            return jsonify({'error': 'Rule not found'}), 404
        
        # 删除规则
        firewall_rules['rules'].remove(rule_to_delete)
        
        # 返回成功响应
        return jsonify({'message': 'Rule deleted successfully'}), 200
    
    except Exception as e:
        # 返回错误响应
        return jsonify({'error': str(e)}), 500

# 定义启动应用程序的函数
def run_app():
    # 启动Quart应用程序
    app.run(debug=True)

if __name__ == '__main__':
    # 调用启动函数
    run_app()