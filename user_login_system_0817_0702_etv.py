# 代码生成时间: 2025-08-17 07:02:57
import quart as q
from quart import jsonify, request

# 假设用户数据存储在字典中，实际应用中应使用数据库
USER_DATA = {
    "user1": "password1",
    "user2": "password2"
}

app = q.Quart(__name__)

"""用户登录验证系统"""

@app.route('/login', methods=['POST'])
async def login():
    # 获取请求中的用户名和密码
    username = await request.form.get("username")
    password = await request.form.get("password")
    
    # 检查用户名和密码是否为空
    if not username or not password:
        return jsonify({"error": "用户名或密码不能为空"}), 400
    
    # 检查用户名是否存在
    if username not in USER_DATA:
        return jsonify({"error": "用户名不存在"}), 404
    
    # 检查密码是否正确
    if USER_DATA.get(username) != password:
        return jsonify({"error": "密码错误"}), 401
    
    # 登录成功，返回成功信息
    return jsonify({"message": "登录成功"}), 200

if __name__ == '__main__':
    app.run(debug=True)