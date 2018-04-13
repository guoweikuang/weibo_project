# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
async crawl weibo

@author guoweikuang
"""

from .weibo import Spider
from .weibo import Parser


def async_crawl_weibo(start_page=1, end_page=5):
    spider = Spider(base_url="https://weibo.cn/gzyhl", name="17317540230", async=True)

    responses = [spider.get_response(page=page) for page in range(start_page, end_page + 1)]
    print(responses[0].text)
    return responses


def run_async_crawl(start_page=1, end_page=5):
    responses = async_crawl_weibo(start_page=start_page, end_page=end_page)
    apps = [Parser(response.text) for response in responses]
    for app in apps:
        app.extract_text()
    apps[0].close_client()
