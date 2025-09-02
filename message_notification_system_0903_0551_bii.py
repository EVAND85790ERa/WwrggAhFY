# 代码生成时间: 2025-09-03 05:51:49
import quart

# 消息通知系统的定义
class MessageNotificationSystem:
    def __init__(self):
        self.messages = []

    # 添加消息到队列
    def add_message(self, message):
        if not message:
            raise ValueError("Message cannot be empty")
        self.messages.append(message)

    # 获取所有消息
    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()  # 清空消息列表
        return messages

# Quart 应用
app = quart.Quart(__name__)

# 实例化消息通知系统
notification_system = MessageNotificationSystem()

# 路由：添加消息
@app.route('/add_message', methods=['POST'])
async def add_message():
    # 获取请求数据
    data = await quart.request.get_json()
    message = data.get('message')

    # 错误处理
    if not message:
        return quart.jsonify({'error': 'No message provided'}), 400

    try:
        notification_system.add_message(message)
        return quart.jsonify({'success': 'Message added successfully'}), 200
    except ValueError as e:
        return quart.jsonify({'error': str(e)}), 400

# 路由：获取消息
@app.route('/get_messages', methods=['GET'])
async def get_messages():
    try:
        messages = notification_system.get_messages()
        if not messages:
            return quart.jsonify({'error': 'No messages available'}), 404
        return quart.jsonify({'messages': messages}), 200
    except Exception as e:
        return quart.jsonify({'error': 'Failed to retrieve messages'}), 500

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)