# 代码生成时间: 2025-08-27 22:50:52
import quart
from quart import jsonify

# 定义主题上下文
class ThemeContext:
    def __init__(self):
        self.current_theme = 'light'

    def switch_theme(self):
        """切换主题，如果当前是'light'则切换到'dark'，反之亦然"""
        if self.current_theme == 'light':
            self.current_theme = 'dark'
        else:
            self.current_theme = 'light'
        return self.current_theme

# 创建主题上下文实例
theme_context = ThemeContext()

# 创建Quart应用
app = quart.Quart(__name__)

# 路由 - 切换主题
@app.route('/switch_theme', methods=['GET'])
async def switch_theme():
    """处理主题切换请求"""
    try:
        # 切换主题
        new_theme = theme_context.switch_theme()
        # 返回新的主题
        return jsonify({'theme': new_theme})
    except Exception as e:
        # 返回错误信息
        return jsonify({'error': str(e)}), 500

# 路由 - 获取当前主题
@app.route('/get_theme', methods=['GET'])
async def get_current_theme():
    """获取当前主题"""
    try:
        # 返回当前的主题
        return jsonify({'theme': theme_context.current_theme})
    except Exception as e:
        # 返回错误信息
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 运行Quart应用
    app.run(debug=True)