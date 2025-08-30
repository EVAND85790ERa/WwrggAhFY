# 代码生成时间: 2025-08-30 20:11:46
import quart as q
from quart import session, jsonify

# 定义可用的主题
AVAILABLE_THEMES = ['light', 'dark']

app = q.Quart(__name__)

# 定义一个路由，用于切换主题
@app.route('/switch-theme', methods=['POST'])
async def switch_theme():
    # 从请求中获取当前选择的主题
    requested_theme = await q.request.get_json()
    if 'theme' not in requested_theme:
        # 如果请求中没有主题，返回错误信息
        return jsonify({'error': 'Missing theme parameter'}), 400
    
    # 验证请求的主题是否可用
    theme = requested_theme['theme']
    if theme not in AVAILABLE_THEMES:
        return jsonify({'error': f'Theme {theme} is not available'}), 400
    
    # 将选择的主题存储在用户的会话中
    session['theme'] = theme
    
    # 返回成功消息
    return jsonify({'message': 'Theme switched successfully'})

# 定义一个路由，用于获取当前的主题
@app.route('/theme')
async def get_current_theme():
    # 从会话中获取当前的主题
    current_theme = session.get('theme', 'light')  # 默认为'light'
    
    # 返回当前主题
    return jsonify({'theme': current_theme})

if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)