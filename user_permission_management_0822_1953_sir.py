# 代码生成时间: 2025-08-22 19:53:05
from quart import Quart, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
from typing import List
from functools import wraps

# Define a simple in-memory user database for demonstration purposes
users_db = {
    'admin': {'password': 'admin123', 'permissions': ['read', 'write', 'delete']},
    'user': {'password': 'user123', 'permissions': ['read']},
}

# Define a User Schema for validation
class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    permissions = fields.List(fields.Str(), required=True)

# Define a Permission Schema for validation
class PermissionSchema(Schema):
    permission = fields.Str(required=True, validate=validate.Length(min=1))

# Initialize the Quart application
app = Quart(__name__)

# A decorator to check user permissions
def check_permission(required_permissions: List[str]):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # Get the username and password from the request
            auth = request.authorization
            if not auth or not auth.username or not auth.password:
                return jsonify({'error': 'Authentication required'}), 401

            # Check user credentials
            user = users_db.get(auth.username)
            if not user or user['password'] != auth.password:
                return jsonify({'error': 'Invalid credentials'}), 403

            # Check if the user has the required permissions
            user_permissions = set(user['permissions'])
            if not user_permissions.intersection(set(required_permissions)):
                return jsonify({'error': 'Insufficient permissions'}), 403

            # Call the decorated function
            return await f(*args, **kwargs)
        return decorated_function
    return decorator

# Route to create a new user
@app.route('/users', methods=['POST'])
async def create_user():
    try:
        user_schema = UserSchema()
        user_data = user_schema.load(await request.get_json())
        users_db[user_data['username']] = {
            'password': user_data['password'],
            'permissions': user_data['permissions']
        }
        return jsonify({'message': 'User created successfully'}), 201
    except ValidationError as err:
        return jsonify({'error': 'Invalid data', 'details': err.messages}), 400

# Route to get user permissions
@app.route('/users/<username>/permissions', methods=['GET'])
@check_permission(required_permissions=[])
def get_user_permissions(username: str):
    user = users_db.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'permissions': user['permissions']})

# Route to update user permissions
@app.route('/users/<username>/permissions', methods=['PUT'])
@check_permission(required_permissions=['write'])
def update_user_permissions(username: str):
    try:
        user_schema = PermissionSchema()
        permission_data = user_schema.load(await request.get_json())
        if username not in users_db:
            return jsonify({'error': 'User not found'}), 404

        # Add the new permission to the user
        users_db[username]['permissions'].append(permission_data['permission'])
        return jsonify({'message': 'Permission updated successfully'}), 200
    except ValidationError as err:
        return jsonify({'error': 'Invalid data', 'details': err.messages}), 400

if __name__ == '__main__':
    app.run()
