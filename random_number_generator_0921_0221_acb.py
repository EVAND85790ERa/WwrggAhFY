# 代码生成时间: 2025-09-21 02:21:27
from quart import Quart, jsonify, request

"""
# NOTE: 重要实现细节
A random number generator service using Quart framework.

This service allows GET requests to generate random numbers within a specified range.
The range can be specified using query parameters 'min' and 'max'.
If no range is specified, it defaults to 0 to 100.
"""

app = Quart(__name__)


@app.route('/generate-random-number', methods=['GET'])
async def generate_random_number():
    "