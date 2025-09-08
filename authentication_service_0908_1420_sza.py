# 代码生成时间: 2025-09-08 14:20:59
from quart import Quart, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Quart(__name__)

# Dummy database for demonstration purposes
DATABASE = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}

@app.route("/login", methods=["POST"])

async def login():
    """Endpoint for user login."""

    username = request.form.get("username")

    password = request.form.get("password")

    if not username or not password:

        return jsonify(error="Missing username or password"), 400

    user_hash = DATABASE.get(username)

    if user_hash is None:

        return jsonify(error="Username not found"), 404

    if not check_password_hash(user_hash, password):

        return jsonify(error="Invalid credentials"), 401

    return jsonify(message="Login successful"), 200

@app.route("/register", methods=["POST"])

async def register():
    """Endpoint for user registration."""

    username = request.form.get("username")

    password = request.form.get("password")

    if not username or not password:

        return jsonify(error="Missing username or password"), 400

    if username in DATABASE:

        return jsonify(error="Username already exists"), 409

    DATABASE[username] = generate_password_hash(password)

    return jsonify(message="User registered successfully"), 201

if __name__ == "__main__":
    app.run(debug=True)
