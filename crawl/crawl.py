# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
async crawl weibo

@author guoweikuang
"""
import time
import random
from multiprocessing import Pool
from crawl.weibo import Spider
from crawl.weibo import Parser


def async_crawl_weibo(start_page=1, end_page=5):
    spider = Spider(base_url="https://weibo.cn/gzyhl", name="17317540230", async=True)
    responses = []
    for page in range(start_page, end_page+1):
        if page % 10 == 0:
            time.sleep(random.randint(0, 2))
        responses.append(spider.get_response(page=page))
    #responses = [spider.get_response(page=page) for page in range(start_page, end_page + 1)]
    # print(responses[0].text)
    return responses


def run_async_crawl(start_page=1, end_page=5):
    """ run async crawl.

    :param start_page:
    :param end_page:
    :return:
    """
    responses = async_crawl_weibo(start_page=start_page, end_page=end_page)
    apps = [Parser(response.text) for response in responses]
    for app in apps:
        app.extract_text()
    apps[0].close_client()


def run_async_crawl_by_day(start_time, days=5):
    """ crawl weibo data by days.

    :param start_time: start date
    :param days: days to crawl
    :return: 貌似这个没有什么意义
    """
    pass


def run_crawl_by_multiprocess(start_page, end_page, pool=4):
    """ run crawl by multiprocessing

    :param pool: 进程池数，设置爬取速度
    :param start_page: start page
    :param end_page: end_page
    :return:
    """
    p = Pool(pool)

    page_num = end_page - start_page + 1
    interval = page_num // pool

    for page in range(1, page_num+1, interval):
        p.apply_async(run_async_crawl, args=(page, page+pool))

    p.close()
    p.join()