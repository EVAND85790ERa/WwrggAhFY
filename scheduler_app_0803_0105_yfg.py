# 代码生成时间: 2025-08-03 01:05:28
import asyncio
import logging
from datetime import datetime
from quart import Quart, jsonify
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 设置日志配置
logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
scheduler = AsyncIOScheduler()
scheduler.start()

# 定义定时任务
def scheduled_job():
    """定时任务函数，每次执行打印当前时间"""
    logging.info(f"Task executed at: {datetime.now()}")

# 添加定时任务
scheduler.add_job(scheduled_job, 'interval', seconds=10)

# 创建API来获取当前时间
@app.route('/time')
async def get_current_time():
    """返回当前时间的API"""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({'current_time': current_time})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# 创建API来添加定时任务
@app.route('/add_job', methods=['POST'])
async def add_job():
    """添加新的定时任务API"""
    try:
        job_id = scheduler.add_job(scheduled_job, 'interval', seconds=10)
        return jsonify({'message': f'Job added with ID: {job_id}')
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# 创建API来移除定时任务
@app.route('/remove_job/<job_id>', methods=['DELETE'])
async def remove_job(job_id):
    """移除指定ID的定时任务API"""
    try:
        if scheduler.remove_job(job_id):
            return jsonify({'message': 'Job removed successfully'})
        else:
            return jsonify({'error': 'Job ID not found'}), 404
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# 程序入口
if __name__ == '__main__':
    app.run(debug=True)
