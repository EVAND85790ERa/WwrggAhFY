# 代码生成时间: 2025-09-06 21:49:16
# notification_service.py

from quart import Quart, jsonify, request
from datetime import datetime

app = Quart(__name__)

# 消息存储列表，用于保存消息通知
messages = []

# 定义路由和视图函数，用于添加消息
@app.route('/add_message', methods=['POST'])
async def add_message():
    """
    添加新的消息到列表中。
    
    :param data: JSON对象包含'message'字段
    :return: 成功添加的消息对象或者错误信息
    """
    try:
        data = await request.get_json()
        if 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        message = {
            'id': len(messages) + 1,
            'message': data['message'],
            'timestamp': datetime.now().isoformat()
        }
        messages.append(message)
        return jsonify(message), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 定义路由和视图函数，用于获取所有消息
@app.route('/get_messages', methods=['GET'])
async def get_messages():
    """
    获取所有保存的消息。
    
    :return: 消息列表
    """
    return jsonify(messages), 200

# 定义路由和视图函数，用于删除消息
@app.route('/delete_message/<int:message_id>', methods=['DELETE'])
async def delete_message(message_id):
    """
    根据ID删除消息。
    
    :param message_id: 要删除的消息的ID
    :return: 成功删除或未找到的消息ID
    """
    global messages
    try:
        messages = [message for message in messages if message['id'] != message_id]
        return jsonify({'message': f'Message {message_id} deleted.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)