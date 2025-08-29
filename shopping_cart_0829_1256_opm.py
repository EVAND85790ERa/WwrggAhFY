# 代码生成时间: 2025-08-29 12:56:51
from quart import Quart, jsonify


def _get_id() -> int:
    """
    A simple function to generate a unique ID.
    This is just a placeholder and should be replaced with a real ID generator.
    """
    id = 0
    while True:
        id += 1
        yield id

id_generator = _get_id()

app = Quart(__name__)


class Cart:
    """
    A class to represent a shopping cart.
    """
    def __init__(self):
        self.items = {}

    def add_item(self, item_id: int, quantity: int):
        """
        Add an item to the cart.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.items[item_id] = self.items.get(item_id, 0) + quantity

    def remove_item(self, item_id: int, quantity: int):
        """
        Remove an item from the cart.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if item_id not in self.items or self.items[item_id] < quantity:
            raise ValueError("Not enough items in the cart.")

        self.items[item_id] -= quantity
        if self.items[item_id] == 0:
            del self.items[item_id]
    
    def get_cart(self):
        """
        Get the current state of the cart.
        """
        return list(self.items.items())


# Global cart instance
cart = Cart()


@app.route("/shopping_cart", methods=["GET", "POST"])
async def shopping_cart():
    """
    A route to handle shopping cart operations.
    """
    if request.method == "POST":
        data = await request.get_json()
        item_id = data.get("item_id")
        quantity = data.get("quantity")

        if item_id is None or quantity is None:
            return jsonify({"error": "Missing item_id or quantity"}), 400

        try:
            quantity = int(quantity)
            item_id = int(item_id)
            cart.add_item(item_id, quantity)
            return jsonify({"message": "Item added to cart"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    else:
        try:
            cart_items = cart.get_cart()
            return jsonify(cart_items), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)