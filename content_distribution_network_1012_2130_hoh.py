# 代码生成时间: 2025-10-12 21:30:00
import quart

# 定义一个简单的内容分发网络 (CDN) 服务
app = quart.Quart(__name__)


# 模拟的内容存储，实际应用中会连接到数据库或文件系统
content_storage = {
    "001": "Hello, this is content 1!",
    "002": "Hello, this is content 2!"
}


# 路由：获取内容
@app.route("/content/<content_id>", methods=["GET"])
async def get_content(content_id):
    # 检查内容是否存在
    if content_id not in content_storage:
        return quart.jsonify({"error": "Content not found"}), 404

    # 返回内容
    return quart.jsonify({"content": content_storage[content_id]})


# 路由：添加内容
@app.route("/content", methods=["POST"])
async def add_content():
    # 获取请求体中的内容
    data = await quart.request.get_json()
    if not data or 'content_id' not in data or 'content' not in data:
        return quart.jsonify({"error": "Missing content data"}), 400

    content_id = data['content_id']
    content = data['content']

    # 检查内容ID是否已存在
    if content_id in content_storage:
        return quart.jsonify({"error": "Content ID already exists"}), 400

    # 添加内容到存储
    content_storage[content_id] = content
    return quart.jsonify({"message": "Content added successfully"}), 201


# 路由：更新内容
@app.route("/content/<content_id>", methods=["PUT"])
async def update_content(content_id):
    # 获取请求体中的内容
    data = await quart.request.get_json()
    if not data or 'content' not in data:
        return quart.jsonify({"error": "Missing content data"}), 400

    content = data['content']

    # 检查内容是否存在
    if content_id not in content_storage:
        return quart.jsonify({"error": "Content not found"}), 404

    # 更新内容
    content_storage[content_id] = content
    return quart.jsonify({"message": "Content updated successfully"}), 200


# 路由：删除内容
@app.route("/content/<content_id>", methods=["DELETE"])
async def delete_content(content_id):
    # 检查内容是否存在
    if content_id not in content_storage:
        return quart.jsonify({"error": "Content not found"}), 404

    # 删除内容
    del content_storage[content_id]
    return quart.jsonify({"message": "Content deleted successfully"}), 200


# 运行程序
if __name__ == '__main__':
    app.run(debug=True)