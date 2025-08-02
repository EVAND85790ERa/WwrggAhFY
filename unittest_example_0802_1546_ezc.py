# 代码生成时间: 2025-08-02 15:46:37
import asyncio
from quart import Quart, jsonify
from quart.testing import QuartClient
import unittest

# 创建一个Quart应用实例
app = Quart(__name__)

# 定义一个路由，返回hello world响应
@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})

# 单元测试类
class TestQuartApp(unittest.IsolatedAsyncioTestCase):
    """
    Quart应用的单元测试类。
    使用QuartClient来进行测试，确保异步测试能正常运行。
    """

    async def asyncSetUp(self):
        # 创建测试客户端
        self.client = await QuartClient(app, loop=self.loop)

    async def asyncTearDown(self):
        # 关闭测试客户端
        await self.client.close()

    # 测试hello路由
    async def test_hello(self):
        # 发起GET请求
        response = await self.client.get('/hello')
        # 验证HTTP状态码
        self.assertEqual(response.status, 200)
        # 验证响应内容
        self.assertEqual(response.json, {'message': 'Hello, World!'})

# 如果是直接运行测试脚本
if __name__ == '__main__':
    unittest.main()
