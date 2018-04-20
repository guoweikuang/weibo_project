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
from handle_text.k_means import run_min_kmeans
from handle_text.k_means import run_mean_shift
from handle_text.build_vsm import run_build_vsm
from handle_text.build_vsm import run_build_vsm_by_file
from handle_text.utils import classify_k_cluster_to_file
from login.login import run_login_weibo
from common.utils import classify_k_cluster_to_redis
from crawl.crawl import run_crawl_by_multiprocess
from classify_text.classify import run_classify
from classify_text.config import corpus_path, seg_path, bag_path, test_bag_path, test_seg_path, test_corpus_path


if __name__ == '__main__':
    #run_classify(corpus_path, seg_path, bag_path, test_bag_path, test_corpus_path, test_seg_path)
    #run_crawl_by_multiprocess(1, 20, 4)
    #run_async_crawl(1, 10)
    now = arrow.utcnow().date()
    start = arrow.utcnow().shift(days=-20).date()
    #rows = run_build_vsm(start_time=start, end_time=now)
    rows = run_build_vsm_by_file()
    labels = run_kmeans(k=4, vsm_name="total")
    #labels = run_kmeans_by_scikit(k=3, vsm_name="total")
    #labels = run_min_kmeans(k=2, vsm_name='total')
    #labels = run_kmeans_by_scikit(k=12, vsm_name='total')
    classify_k_cluster_to_redis(labels=labels, texts=rows)
    classify_k_cluster_to_file(labels=labels, texts=rows)