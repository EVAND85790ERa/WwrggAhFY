# 代码生成时间: 2025-08-14 14:38:17
import quart
from quart import request
import requests
from bs4 import BeautifulSoup
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

# 创建Quart应用
app = quart.Quart(__name__)


@app.route('/scrape', methods=['GET'])
async def scrape_content():
    """
    抓取网页内容的路由
    
    参数:
        url: 要抓取的网页URL
    返回:
        抓取的网页内容
    """
    try:
        # 获取请求参数
        url = request.args.get('url')
        if not url:
            return quart.jsonify({'error': 'URL is required'}), 400
        
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        response.raise_for_status() # 检查请求是否成功
        
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取网页的标题
        title = soup.title.string if soup.title else 'No title found'
        
        # 获取网页的主体内容
        body = soup.find('body').text if soup.find('body') else 'No body found'
        
        # 返回抓取的内容
        return quart.jsonify({'title': title, 'body': body})
    
    except requests.RequestException as e:
        # 处理请求异常
        logging.error(f'Request error: {e}')
        return quart.jsonify({'error': 'Request failed'}), 500
    
    except Exception as e:
        # 处理其他异常
        logging.error(f'Error: {e}')
        return quart.jsonify({'error': 'An error occurred'}), 500


if __name__ == '__main__':
    # 运行Quart应用
    app.run(debug=True)