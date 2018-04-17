# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
程序入口

@author guoweikuang
"""
import arrow

from crawl.crawl import run_async_crawl
from handle_text.k_means import run_kmeans
from handle_text.k_means import run_kmeans_by_scikit
from handle_text.build_vsm import run_build_vsm
from handle_text.utils import classify_k_cluster_to_file
from login.login import run_login_weibo
from common.utils import classify_k_cluster_to_redis
from pprint import pprint

if __name__ == '__main__':
    #run_async_crawl(1, 10)
    now = arrow.utcnow().date()
    start = arrow.utcnow().shift(days=-10).date()
    rows = run_build_vsm(start_time=start, end_time=now)
    #pprint([row[0] for row in rows])
    labels = run_kmeans(k=4, vsm_name="total")
    labels = run_kmeans_by_scikit(k=4, vsm_name="total")
    classify_k_cluster_to_redis(labels=labels, texts=rows)
    classify_k_cluster_to_file(labels=labels, texts=rows)