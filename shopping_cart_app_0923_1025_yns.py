# 代码生成时间: 2025-09-23 10:25:17
from quart import Quart, jsonify, request, session

# 定义一个简单的购物车类
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, quantity):
        """添加商品到购物车"""
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id):
        """从购物车中移除商品"""
        if item_id in self.items:
            del self.items[item_id]

    def update_quantity(self, item_id, quantity):
        """更新购物车中的商品数量"""
        if item_id in self.items:
            self.items[item_id] = quantity
        else:
            raise ValueError("Item not in cart")

    def get_cart(self):
        """获取购物车中所有商品"""
        return self.items

# 创建一个全局的购物车实例
cart = ShoppingCart()

# 初始化Quart应用
app = Quart(__name__)

# 购物车路由
@app.route("/add_to_cart", methods=["POST"])
async def add_to_cart():
    # 从请求中获取商品ID和数量
    item_id = request.json.get("item_id")
    quantity = request.json.get("quantity")

    # 检查输入是否有效
    if item_id is None or quantity is None or quantity < 0:
        return jsonify(error="Invalid input"), 400

    # 添加商品到购物车
    try:
        cart.add_item(item_id, quantity)
        return jsonify(message="Item added to cart"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/remove_from_cart", methods=["POST"])
async def remove_from_cart():
    # 从请求中获取商品ID
    item_id = request.json.get("item_id")

    # 检查输入是否有效
    if item_id is None:
        return jsonify(error="Invalid input"), 400

    # 从购物车中移除商品
    try:
        cart.remove_item(item_id)
        return jsonify(message="Item removed from cart"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/update_cart", methods=["POST"])
async def update_cart():
    # 从请求中获取商品ID和数量
    item_id = request.json.get("item_id")
    quantity = request.json.get("quantity")

    # 检查输入是否有效
    if item_id is None or quantity is None or quantity < 0:
        return jsonify(error="Invalid input"), 400

    # 更新购物车中的商品数量
    try:
        cart.update_quantity(item_id, quantity)
        return jsonify(message="Item quantity updated"), 200
    except ValueError as e:
        return jsonify(error=str(e)), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/get_cart")
async def get_cart():
    # 获取购物车中所有商品
    try:
        cart_items = cart.get_cart()
        return jsonify(cart_items), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)