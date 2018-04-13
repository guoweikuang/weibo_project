# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
程序入口

@author guoweikuang
"""
import arrow

from crawl.crawl import run_async_crawl
from handle_text.k_means import run_kmeans
from handle_text.build_vsm import run_build_vsm
from login.login import run_login_weibo


if __name__ == '__main__':
    run_async_crawl(1, 10)
    now = arrow.utcnow().date()
    start = arrow.utcnow().shift(days=-2).date()
    run_build_vsm(start_time=start, end_time=now)
    run_kmeans(k=4, vsm_name="total")
