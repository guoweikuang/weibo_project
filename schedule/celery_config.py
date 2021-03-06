# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~
Celery cofing module

@author guoweikuang
"""
from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
CELERY_TASK_SERIALIZER = "msgpack"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
CELERY_TIMEZONE = 'Asia/Shanghai'


CELERYBEAT_SCHEDULE = {
    "crawl": {
        'task': "schedule.tasks.schedule_async_crawl",
        "schedule": timedelta(hours=5),
        "args": (1, 10),
    },
    "sensitive": {
        "task": "schedule.tasks.schedule_get_sensitive",
        "schedule": timedelta(hours=5),
    }

}


# CELERYBEAT_SCHEDULE = {
#     "sensitive": {
#         "task": "schedule.tasks.schedule_get_sensitive",
#         "schedule": timedelta(hours=2),
#     }
# }