# 代码生成时间: 2025-08-26 23:41:30
import quart
from quart import request
from quart import jsonify

# 引入plotly库绘制图表
import plotly.graph_objects as go

# 交互式图表生成器应用
class InteractiveChartGenerator:
    def __init__(self):
        self.app = quart.Quart(__name__)

    # 路由：提供GET请求来生成图表
    @self.app.route('/chart', methods=['GET'])
    async def generate_chart(self):
        # 获取查询参数
        query = request.args
        x = query.get('x')
        y = query.get('y')
        
        # 错误处理：检查参数
        if not x or not y:
            return jsonify({'error': 'Missing x or y parameter'}), 400
        
        # 尝试将参数转换为数值，用于绘制图表
        try:
            x = list(map(float, x.split(',')))
            y = list(map(float, y.split(',')))
        except ValueError:
            return jsonify({'error': 'Invalid x or y parameter format'}), 400
        
        # 创建图表
        chart = go.Figure(data=[go.Scatter(x=x, y=y)])
        chart.update_layout(title='Interactive Chart', xaxis_title='X Axis', yaxis_title='Y Axis')
        
        # 将图表保存为HTML文件
        html_div = chart.to_html(full_html=False)
        
        # 返回图表的HTML代码
        return html_div

# 实例化并运行应用
if __name__ == '__main__':
    generator = InteractiveChartGenerator()
    generator.app.run(debug=True)