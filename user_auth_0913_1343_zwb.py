# 代码生成时间: 2025-09-13 13:43:11
import quart
from quart import jsonify, request, abort
from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

# User model to hold user data
class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    # Check if the password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User schema for deserialization
class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4))
    password = fields.Str(required=True, validate=validate.Length(min=8))

# API route for user authentication
@app.route('/login', methods=['POST'])
async def login():
    try:
        # Deserialize and validate input data
        user_schema = UserSchema()
        incoming_data = await request.get_json()
        data = user_schema.load(incoming_data)

        # Find user in 'database'
        user = users.get(data['username'])
        if user and user.check_password(data['password']):
            return jsonify({'message': 'Login successful'}), 200
        else:
            abort(401)  # Unauthorized access
    except ValidationError as err:
        return jsonify({'message': 'Invalid data', 'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# In-memory 'database' of users
users = {}

# Register a new user
@app.route('/register', methods=['POST'])
async def register():
    try:
        # Deserialize and validate input data
        user_schema = UserSchema()
        incoming_data = await request.get_json()
        data = user_schema.load(incoming_data)

        # Check if user already exists
        if data['username'] in users:
            abort(409)  # Conflict

        # Create and store user in 'database'
        new_user = User(data['username'], data['password'])
        users[data['username']] = new_user

        return jsonify({'message': 'User registered successfully'}), 201
    except ValidationError as err:
        return jsonify({'message': 'Invalid data', 'errors': err.messages}), 400

# Run the Quart app
if __name__ == '__main__':
    app.run(debug=True)