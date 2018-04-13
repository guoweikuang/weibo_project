# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
tasks module

@author guoweiuang
"""
from schedule.app import app
from crawl.crawl import async_crawl_weibo


@app.task
def schedule_async_crawl(start_page, end_page):
    async_crawl_weibo(start_page, end_page)




