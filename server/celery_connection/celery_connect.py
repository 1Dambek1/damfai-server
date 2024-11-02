# from celery import Celery
# from celery.schedules import crontab

# import asyncio

# from .celery_config import config

# from running.running_utils import run_check_race_status


# celery = Celery('tasks', broker=f'{config.celery.BROKER_URL}')

# celery.conf.update({
#     'timezone': 'UTC',
#     'beat_schedule': {
#         'check_race_status_every_minute': {  # Название периодической задачи
#             'task': 'tasks.check_race_status',  # Имя задачи
#             'schedule': crontab(minute='*/1'),  # Интервал (каждую минуту)
#         },
#     },
# })


# @celery.task(name='tasks.check_race_status')
# def check_race_status():
#     asyncio.run(run_check_race_status())
# ____________FUTURE__________________
