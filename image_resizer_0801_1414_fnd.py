# 代码生成时间: 2025-08-01 14:14:24
import os
from quart import Quart, request, jsonify
from PIL import Image

# 定义一个Quart应用
app = Quart(__name__)

# 定义一个路由，用于处理文件上传和尺寸调整
@app.route("/resize", methods=["POST"])
async def resize_images():
    # 获取上传的文件
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    # 验证文件类型
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file.mimetype not in ['image/jpeg', 'image/png']:
        return jsonify({"error": "Only JPEG and PNG images are supported"}), 400
    
    # 读取文件内容
    image = Image.open(file.stream)
    
    # 获取新尺寸
    try:
        new_width = int(request.form.get('width', '0'))
        new_height = int(request.form.get('height', '0'))
    except ValueError:
        return jsonify({"error": "Invalid dimensions"}), 400
    
    # 调整尺寸
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    
    # 保存调整后的图片
    output_path = os.path.join(os.getcwd(), 'resized_images')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    output_filename = os.path.join(output_path, file.filename)
    resized_image.save(output_filename, image.format)
    
    return jsonify({"message": "Image resized successfully", "path": output_filename}), 200

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)