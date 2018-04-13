# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
celery instance module

@author guoweikuang
"""
from celery import Celery


app = Celery('schedule', include=['schedule.tasks'])
app.config_from_object('schedule.celery_config')


if __name__ == '__main__':
    app.start()