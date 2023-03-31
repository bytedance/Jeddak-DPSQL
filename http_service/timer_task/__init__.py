from flask_apscheduler import APScheduler
from http_service.timer_task.budget_task import budget_recover


scheduler = APScheduler()


# init APScheduler
def init_scheduler(app):
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.add_job(func=budget_recover, id='budget_recover', trigger='cron', hour=00, minute=00, misfire_grace_time=900)


def start_scheduler():
    scheduler.start()
