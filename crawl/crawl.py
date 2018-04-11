# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
async crawl weibo

@author guoweikuang
"""

from .weibo import Spider


def async_crawl_weibo(start_page=1, end_page=5):
    spider = Spider(base_url="https://weibo.cn/gzyhl", name="17317540230", async=True)

    responses = [spider.get_response(page=page) for page in range(start_page, end_page + 1)]
    print(responses[0].text)
    return responses
