# 代码生成时间: 2025-08-06 02:45:16
import quart
from quart import request, jsonify
from cryptography.fernet import Fernet

# 密钥生成
def generate_key():
    """生成密钥并返回"""
    return Fernet.generate_key()

# 加密密码
def encrypt_password(password, key):
    """使用提供的密钥加密密码"""
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()

# 解密密码
def decrypt_password(encrypted_password, key):
    """使用提供的密钥解密密码"""
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

# 创建Quart应用
app = quart.Quart(__name__)

# 密钥存储
key = generate_key()

@app.route('/api/encrypt', methods=['POST'])
async def encrypt():
    """加密密码的API接口"""
    try:
        data = await request.get_json()
        if 'password' not in data:
            return jsonify({'error': 'Missing password'}), 400

        encrypted = encrypt_password(data['password'], key)
        return jsonify({'encrypted': encrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
async def decrypt():
    """解密密码的API接口"""
    try:
        data = await request.get_json()
        if 'encrypted_password' not in data:
            return jsonify({'error': 'Missing encrypted password'}), 400

        decrypted = decrypt_password(data['encrypted_password'], key)
        return jsonify({'decrypted': decrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)