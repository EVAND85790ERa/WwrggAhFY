# 代码生成时间: 2025-08-24 03:59:00
import quart
from quart import jsonify, request

# 定义订单状态枚举类
class OrderStatus:
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

# 订单处理类
class OrderProcessor:
    def __init__(self):
        self.orders = {}  # 存储订单信息

    def create_order(self, order_id, product_name):
        """创建新订单"""
        self.orders[order_id] = {'product_name': product_name, 'status': OrderStatus.PENDING}
        return {'order_id': order_id, 'status': 'created'}

    def cancel_order(self, order_id):
        """取消订单"""
        if order_id in self.orders:
            self.orders[order_id]['status'] = OrderStatus.CANCELLED
            return {'order_id': order_id, 'status': 'cancelled'}
        else:
            raise ValueError('Order not found')

    def complete_order(self, order_id):
        """完成订单"""
        if order_id in self.orders:
            self.orders[order_id]['status'] = OrderStatus.COMPLETED
            return {'order_id': order_id, 'status': 'completed'}
        else:
            raise ValueError('Order not found')

    def get_order_status(self, order_id):
        """获取订单状态"""
        if order_id in self.orders:
            return {'order_id': order_id, 'status': self.orders[order_id]['status']}
        else:
            raise ValueError('Order not found')

# Quart应用
app = quart.Quart(__name__)

@app.route('/create_order', methods=['POST'])
async def create_order():
    order_id = request.json.get('order_id')
    product_name = request.json.get('product_name')
    if not order_id or not product_name:
        return jsonify({'error': 'Missing order_id or product_name'}), 400
    try:
        result = OrderProcessor().create_order(order_id, product_name)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cancel_order/<string:order_id>', methods=['PUT'])
async def cancel_order(order_id):
    try:
        result = OrderProcessor().cancel_order(order_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/complete_order/<string:order_id>', methods=['PUT'])
async def complete_order(order_id):
    try:
        result = OrderProcessor().complete_order(order_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/get_order_status/<string:order_id>', methods=['GET'])
async def get_order_status(order_id):
    try:
        result = OrderProcessor().get_order_status(order_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)