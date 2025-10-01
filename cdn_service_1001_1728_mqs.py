# 代码生成时间: 2025-10-01 17:28:44
import asyncio
from quart import Quart, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

# Create a Quart application instance
app = Quart(__name__)

# Define a dictionary to act as a simple content delivery network (CDN)
cdn_cache = {}

# Helper function to get the content from the CDN cache
def get_from_cdn(key):
    """Retrieves content from the CDN cache.

    Args:
        key (str): The key of the content to retrieve.

    Returns:
        str: The content associated with the key, or None if not found."""
    return cdn_cache.get(key)

# Helper function to add content to the CDN cache
def add_to_cdn(key, content):
    """Adds content to the CDN cache.

    Args:
        key (str): The key for the content to store.
        content (str): The content to store."""
    cdn_cache[key] = content

# Route to serve content from the CDN
@app.route('/serve/<key>', methods=['GET'])
async def serve_content(key):
    """Serves content from the CDN cache.

    Args:
        key (str): The key of the content to serve.

    Returns:
        str: The content associated with the key.

    Raises:
        NotFound: If the content is not found in the CDN cache."""
    content = get_from_cdn(key)
    if content is None:
        raise NotFound(description=f"Content not found for key: {key}")
    return content

# Route to add content to the CDN
@app.route('/add/<key>', methods=['POST'])
async def add_content(key):
    """Adds content to the CDN cache.

    Args:
        key (str): The key for the content to add.

    Returns:
        str: A success message.

    Raises:
        BadRequest: If the request is missing a JSON body or the body is not a string."""
    content = await request.get_json()
    if content is None or not isinstance(content, str):
        raise BadRequest(description="Request body must be a JSON string.")
    add_to_cdn(key, content)
    return jsonify({'message': 'Content added to CDN successfully'})

# Run the application
if __name__ == '__main__':
    asyncio.run(app.run(debug=True))
