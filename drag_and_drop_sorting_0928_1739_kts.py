# 代码生成时间: 2025-09-28 17:39:44
import quart
from quart import render_template_string

# 定义一个HTML模板用于拖拽排序组件
DND_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Drag and Drop Sorting</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <style>
        #sortable { list-style-type: none; margin: 0; padding: 0; width: 60%; }
        #sortable li { margin: 3px; padding: 5px; font-size: 1.2em; }
    </style>
</head>
<body>
    <h2>Drag and Drop Sorting</h2>
    <ul id="sortable">
        <li class="ui-state-default" v-model="item" v-for="item in items">{item}</li>
    </ul>
    <button onclick="saveOrder()">Save Order</button>
    <script>
        function saveOrder() {
            var sortedList = $.map($('#sortable').sortable('toArray'), function(id){ return id; });
            fetch('/save-order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(sortedList),
            }).then(response => response.json())
              .then(data => console.log(data))
              .catch(error => console.error('Error:', error));
        }
        $(function() {
            $("#sortable").sortable();
        });
    </script>
</body>
</html>
"""

app = quart.Quart(__name__)

# 定义根路由，返回拖拽排序组件的HTML页面
@app.route('/')
async def index():
    return render_template_string(DND_TEMPLATE)

# 定义POST路由，用于接收排序后的数据并处理
@app.route('/save-order', methods=['POST'])
async def save_order():
    try:
        # 获取请求体中的JSON数据
        data = await quart.request.get_json()
        # 处理排序数据，这里只是打印出来
        print(data)
        # 返回成功响应
        return {'status': 'success', 'message': 'Order saved successfully'}
    except Exception as e:
        # 错误处理
        print(f"Error: {e}")
        return {'status': 'error', 'message': 'Failed to save order'}, 400

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
