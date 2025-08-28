# 代码生成时间: 2025-08-28 13:58:29
import quart
from quart import jsonify
import requests
from urllib.parse import urlparse

# 定义一个函数来检查URL的有效性
def is_url_valid(url):
    """
    检查给定的URL是否有效。

    :param url: 要检查的URL字符串。
    :return: 布尔值，True表示URL有效，False表示无效。
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc) and bool(parsed_url.scheme)

# 创建一个Quart应用
app = quart.Quart(__name__)

# 为Quart应用定义一个路由，用于URL验证
@app.route('/validate', methods=['POST'])
async def validate_url():
    """
    验证POST请求中的URL。

    :return: JSON响应，包含URL有效性的检查结果。
    """
    # 获取请求中的URL数据
    url_data = await quart.request.get_json()
    url_to_check = url_data.get('url')
    if url_to_check is None:
        # 当请求体中没有包含url字段时，返回错误
        return jsonify({'error': 'Missing URL parameter'})
    
    # 检查URL是否有效
    is_valid = is_url_valid(url_to_check)
    
    # 返回检查结果
    return jsonify({'url': url_to_check, 'valid': is_valid})

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
