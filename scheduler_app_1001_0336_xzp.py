# 代码生成时间: 2025-10-01 03:36:21
import asyncio
from quart import Quart, jsonify
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# 定义一个 Quartz 应用
app = Quart(__name__)
scheduler = AsyncIOScheduler()
scheduler.start()

# 定义定时任务调度器
class Scheduler:
    def __init__(self):
        self.scheduler = scheduler

    def add_job(self, func, trigger, args=None, kwargs=None, id=None, name=None, replace_existing=False):
        self.scheduler.add_job(func, trigger, args=args, kwargs=kwargs, id=id, name=name, replace_existing=replace_existing)

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def pause_job(self, job_id):
        self.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        self.scheduler.resume_job(job_id)

# 定时任务调度器实例
scheduler_app = Scheduler()

# 添加定时任务
# 每5秒执行一次
@scheduler_app.scheduler.scheduled_job(IntervalTrigger(seconds=5), id='my_job', name='My Scheduled Job')
async def my_job():
    print('Job executed')

# 创建 API 接口来添加新的定时任务
@app.route('/add_job', methods=['POST'])
async def add_new_job():
    data = await request.get_json()
    func_name = data.get('func')
    trigger_type = data.get('trigger')
    trigger_args = data.get('args')
    id = data.get('id')
    name = data.get('name')

    if not all([func_name, trigger_type, trigger_args]):
        return jsonify({'error': 'Missing required parameters'}), 400

    # 动态调用函数
    if func_name == 'my_job':
        scheduler_app.add_job(my_job, trigger_type, args=trigger_args, id=id, name=name)
        return jsonify({'message': 'Job added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid function name'}), 400

# 启动服务
if __name__ == '__main__':
    app.run(debug=True)
