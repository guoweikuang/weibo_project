# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
async crawl weibo

@author guoweikuang
"""

from .weibo import Spider


def async_crawl_weibo(pages=5):
    spider = Spider(base_url="https://weibo.cn/gzyhl", name="17317540230", async=True)

    responses = [spider.get_response(page=page) for page in range(1, pages+1)]
    print(responses[0].text)
    return responses
