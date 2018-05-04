# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
tasks module

@author guoweiuang
"""
from schedule.app import app
from crawl.crawl import async_crawl_weibo
from handle_text.sensitive import run_schedule_text_from_mysql
from handle_text.sensitive import run_sensitive


@app.task
def schedule_async_crawl(start_page, end_page):
    async_crawl_weibo(start_page, end_page)


@app.task
def schedule_get_sensitive():
    rows = run_schedule_text_from_mysql()
    run_sensitive(rows=rows)

