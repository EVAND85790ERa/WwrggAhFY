# 代码生成时间: 2025-08-19 16:45:48
import quart
from cryptography.fernet import Fernet

"""
Password Encryption/Decryption Tool

This tool uses the Quart framework to create a web service for
password encryption and decryption. It utilizes the cryptography
library to safely encrypt and decrypt passwords.
"""

# Generate a key for encryption and decryption
# The key should be kept secret and secure
key = Fernet.generate_key()
cipher_suite = Fernet(key)

app = quart.Quart(__name__)

@app.route('/encrypt/<password>', methods=['GET'])
async def encrypt_password(password: str):
    """Encrypts the given password using the Fernet cipher."""
    try:
        encrypted_password = cipher_suite.encrypt(password.encode())
        return {'encrypted_password': encrypted_password.decode()}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/decrypt/<encrypted_password>', methods=['GET'])
async def decrypt_password(encrypted_password: str):
    """Decrypts the given encrypted password using the Fernet cipher."""
    try:
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
        return {'decrypted_password': decrypted_password.decode()}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run()

# Note: The encryption key should be stored securely and not hardcoded
#       into the source code. For the purpose of this example, the key
#       is generated and used directly. In a production environment,
#       consider using environment variables or a secure key management
#       system to store the encryption key.