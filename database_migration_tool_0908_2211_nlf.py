# 代码生成时间: 2025-09-08 22:11:31
import quart
from quart import jsonify
from quart_sqlalchemy import SQLAlchemy
import os
import alembic.config
import alembic
from alembic import command
from alembic import script
from your_application_package import create_app  # 导入你的应用的初始化函数
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义数据库配置
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # 更新为你的数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# 初始化数据库
db = SQLAlchemy()

# 创建Quart应用
app = create_app(Config)

# 注册数据库
app.db = db

# 迁移命令
@app.route('/migrate', methods=['POST'])
async def migrate():
    try:
        # 获取数据库URI
        alembic_cfg = alembic.config.Config(
            os.path.join(os.path.dirname(__file__), 'alembic.ini'))
        
        # 执行迁移命令
        command.upgrade(alembic_cfg, 'head')
        
        # 返回迁移成功的消息
        return jsonify({'status': 'success', 'message': 'Database migration successful'})
    except Exception as e:
        # 记录错误信息
        logger.error(f'Database migration failed: {e}')
        
        # 返回迁移失败的消息
        return jsonify({'status': 'error', 'message': f'Database migration failed: {e}'})

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
