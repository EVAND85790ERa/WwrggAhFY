# 代码生成时间: 2025-08-03 11:21:25
from quart import Quart, request, jsonify
from math import sqrt, sin, cos, tan, log, log10, exp, pi

"""
Math Toolkit API
A simple API that provides various mathematical operations.
"""
app = Quart(__name__)

# Define a dictionary to map strings to math functions
MATH_FUNCTIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b if b != 0 else "Cannot divide by zero",
    "sqrt": lambda n: sqrt(n) if n >= 0 else "Negative number given",
    "sin": lambda n: sin(n),
    "cos": lambda n: cos(n),
    "tan": lambda n: tan(n),
    "log": lambda n: log(n),
    "log10": lambda n: log10(n),
    "exp": lambda n: exp(n),
    "pow": lambda a, b: a ** b,
}


# Endpoint to handle math operations
@app.route("/calculate", methods=["POST"])
async def calculate():
    data = await request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    operation = data.get("operation")
    if operation not in MATH_FUNCTIONS:
        return jsonify({"error": f"Unsupported operation: {operation}"}), 400

    try:
        a = float(data.get("a"))
        b = data.get("b")
        # If b is not provided, assume it's a unary operation
        if b is None:
            result = MATH_FUNCTIONS[operation](a)
        else:
            b = float(b)
            result = MATH_FUNCTIONS[operation](a, b)
    except ValueError:
        return jsonify({"error": "Invalid input values"}), 400
    except ZeroDivisionError:
        return jsonify({"error": "Division by zero"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})


# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run()
