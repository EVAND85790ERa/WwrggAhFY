# 代码生成时间: 2025-08-02 06:11:15
import asyncio
from quart import Quart, jsonify
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

# 初始化Quart应用
app = Quart(__name__)
scheduler = AsyncIOScheduler(jobstores={"default": MemoryJobStore()},
                           executors={"default": AsyncIOExecutor()},
                           auto_start=False)

# 配置Quart路由
@app.route('/run_job/<job_id>')
async def run_job(job_id: str):
    """
    手动触发一个定时任务。
    :param job_id: 任务的ID
    :return: JSON响应
    """
    job = scheduler.get_job(job_id)
    if job:
        await scheduler.start()
        job.remove(quiet=True)
        scheduler.add_job(func=job.func, trigger=job.trigger, **job.kwargs)
        return jsonify({'message': f'Job {job_id} triggered.'}), 200
    else:
        return jsonify({'error': 'Job not found.'}), 404

# 启动定时调度器
@app.before_serving
def start_scheduler():
    scheduler.start()

# 定义一个示例任务
async def example_task():
    print('Example task executed.')

# 添加任务到调度器
scheduler.add_job(example_task, CronTrigger.from_crontab('* * * * *'))  # 每分钟执行一次

# 启动Quart应用
if __name__ == '__main__':
    app.run(debug=True)
