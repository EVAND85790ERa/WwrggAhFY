# 代码生成时间: 2025-08-24 00:22:27
import quart

# Define a ShoppingCart class to manage the cart operations
defining the structure of a cart item
class CartItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

# Define the ShoppingCart class to handle cart operations
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product_id, quantity):
        """Add an item to the cart or update the quantity if it already exists."""
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
        else:
            self.items[product_id] = {'quantity': quantity}

    def remove_item(self, product_id, quantity):
        """Remove the specified quantity of an item from the cart."""
        if product_id in self.items:
            if self.items[product_id]['quantity'] <= quantity:
                del self.items[product_id]
            else:
                self.items[product_id]['quantity'] -= quantity
        else:
            raise ValueError("Item not found in the cart.")

    def get_cart(self):
        """Return the current state of the cart."""
        return list(self.items.values())

# Define the Quart app
app = quart.Quart(__name__)

# Initialize the shopping cart
cart = ShoppingCart()

# Endpoint to add an item to the cart
@app.route("/add", methods=["POST"])
async def add_item_to_cart():
    try:
        data = await quart.request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity or not isinstance(quantity, int):
            return quart.jsonify({'error': 'Invalid data provided.'}), 400

        cart.add_item(product_id, quantity)
        return quart.jsonify({'message': 'Item added to cart successfully.'}), 200
    except Exception as e:
        return quart.jsonify({'error': str(e)}), 500

# Endpoint to remove an item from the cart
@app.route("/remove", methods=["POST"])
async def remove_item_from_cart():
    try:
        data = await quart.request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity or not isinstance(quantity, int):
            return quart.jsonify({'error': 'Invalid data provided.'}), 400

        cart.remove_item(product_id, quantity)
        return quart.jsonify({'message': 'Item removed from cart successfully.'}), 200
    except ValueError as ve:
        return quart.jsonify({'error': str(ve)}), 404
    except Exception as e:
        return quart.jsonify({'error': str(e)}), 500

# Endpoint to get the current cart
@app.route("/", methods=["GET"])
async def get_cart_items():
    try:
        cart_items = cart.get_cart()
        return quart.jsonify(cart_items), 200
    except Exception as e:
        return quart.jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)