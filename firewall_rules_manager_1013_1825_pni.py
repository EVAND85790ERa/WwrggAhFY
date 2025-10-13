# 代码生成时间: 2025-10-13 18:25:09
import quart
from quart import jsonify, request

# 定义一个简单的防火墙规则模型
class FirewallRule:
    def __init__(self, id, source_ip, destination_ip, protocol, port):
        self.id = id
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.protocol = protocol
        self.port = port

    def to_dict(self):
        """将FirewallRule对象转换为字典"""
        return {
            "id": self.id,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "protocol": self.protocol,
            "port": self.port
        }

# 创建一个类来管理防火墙规则
class FirewallRulesManager:
    def __init__(self):
        self.rules = []
        self.next_id = 1

    def add_rule(self, source_ip, destination_ip, protocol, port):
        """添加一个新的防火墙规则"""
        rule = FirewallRule(self.next_id, source_ip, destination_ip, protocol, port)
        self.rules.append(rule)
        self.next_id += 1
        return rule.to_dict()

    def get_rule(self, rule_id):
        """根据ID获取防火墙规则"""
        for rule in self.rules:
            if rule.id == rule_id:
                return rule.to_dict()
        return None

    def delete_rule(self, rule_id):
        """根据ID删除防火墙规则"""
        self.rules = [rule for rule in self.rules if rule.id != rule_id]

    def update_rule(self, rule_id, source_ip=None, destination_ip=None, protocol=None, port=None):
        """根据ID更新防火墙规则"""
        for rule in self.rules:
            if rule.id == rule_id:
                if source_ip:
                    rule.source_ip = source_ip
                if destination_ip:
                    rule.destination_ip = destination_ip
                if protocol:
                    rule.protocol = protocol
                if port:
                    rule.port = port
                return rule.to_dict()
        return None

# 创建一个Quart应用程序
app = quart.Quart(__name__)

# 实例化防火墙规则管理器
rules_manager = FirewallRulesManager()

# 添加防火墙规则的路由
@app.route("/add_rule", methods=["POST"])
async def add_firewall_rule():
    data = await request.get_json()
    if not data or "source_ip" not in data or "destination_ip" not in data or "protocol" not in data or "port" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    rule = rules_manager.add_rule(
        data["source_ip"], data["destination_ip"], data["protocol"], data["port"]
    )
    return jsonify(rule), 201

# 获取防火墙规则的路由
@app.route("/rule/<int:rule_id>", methods=["GET", "DELETE", "PUT"])
async def handle_rule(rule_id):
    rule = rules_manager.get_rule(rule_id)
    if rule is None:
        return jsonify({"error": "Rule not found"}), 404
    if request.method == "GET":
        return jsonify(rule)
    elif request.method == "DELETE":
        rules_manager.delete_rule(rule_id)
        return jsonify({"message": "Rule deleted"}), 200
    elif request.method == "PUT":
        data = await request.get_json()
        updated_rule = rules_manager.update_rule(rule_id, **data)
        if updated_rule is None:
            return jsonify({"error": "Rule not found"}), 404
        return jsonify(updated_rule), 200

if __name__ == "__main__":
    app.run(debug=True)