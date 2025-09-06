# 代码生成时间: 2025-09-06 17:48:51
import quart
from hashlib import sha256, sha1, md5
from quart import request, jsonify

"""
哈希值计算工具
提供API接口，接受输入字符串，返回其SHA-256, SHA-1和MD5哈希值"""

app = quart.Quart(__name__)

"