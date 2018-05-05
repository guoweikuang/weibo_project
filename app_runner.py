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
from utils import run_first_cluster
from utils import run_second_cluster
from utils import run_hot_topic
from utils import run_cluster
from login.login import run_login_weibo
from common.utils import classify_k_cluster_to_redis
from crawl.crawl import run_crawl_by_multiprocess
from classify_text.classify import run_classify
from classify_text.main import run_classify_text
from classify_text.config import corpus_path, seg_path, bag_path, test_bag_path, test_seg_path, test_corpus_path
from draw_chart import run_draw_chart, run_draw_top_keyword_barh, run_draw_pie
from handle_text.sensitive import run_sensitive
from classify_text.utils import read_text_old_mysql, save_to_file
from utils import run_old_all_process, run_new_all_process
from handle_text.hot_topic import list_hot_topic
from utils import run_old_second_all_process
from handle_text.draw_chart import run_draw_pie


if __name__ == '__main__':

    # 登录模块
    #run_login_weibo(username='15602200534', password='guoweikuang2018')

    #   异步爬取模块
    #run_crawl_by_multiprocess(1, 20, 4)
    #run_async_crawl(1, 10)

    #  读取数据并构建向量空间模型
    now = arrow.utcnow().date()
    start = arrow.utcnow().shift(days=-120).date()
    rows, texts = run_build_vsm(start_time=start, end_time=now)
    rows = run_build_vsm_by_file()

    #   读取旧数据库模块，用于test
    end_time = arrow.get("2016-10-30")
    rows = read_text_old_mysql(end_time, days=30, database='weibo')
    #save_to_file('old_mysql', rows)

    #   分类模块
    #run_classify_text(rows)

    #   k-means 聚类模块
    #labels = run_kmeans(k=4, vsm_name="total")
    labels = run_kmeans_by_scikit(k=3, vsm_name="total")
    #labels = run_min_kmeans(k=2, vsm_name='total')

    #  画图模块
    run_draw_pie(db=2)
    #run_draw_chart(db=1)
    #run_draw_top_keyword_barh(db=2)
    #run_draw_cluster_chart(db=1)

    #   对聚类结果进行归类模块
    #classify_k_cluster_to_redis(labels=labels, texts=rows)
    #classify_k_cluster_to_file(labels=labels, texts=rows)

    #   敏感词发现模块
    results = []
    for row in rows:
        results.append([row[0], row[1], row[2], row[3].strip()])
    #run_sensitive(rows=results)

    #   一次及二次聚类模块
    #run_second_cluster()
    #run_first_cluster('1', '1')
    start = '2018-03-01'
    end = '2018-04-29'
    end_time = arrow.get("2016-10-30")
    #run_new_all_process(start, end, k=5)
    #run_old_all_process(end_time)
    #run_cluster(start, end, k=7)
    #run_old_all_process(end_time)
    #list_hot_topic(db=1)
    #run_old_second_all_process(start_time='1', end_time=end_time)

    #  热点话题热度值计算模块
    #run_hot_topic()

    # 分类并进行正确归类
    #run_classify_text(rows)
    #run_classify(corpus_path, seg_path, bag_path, test_bag_path, test_corpus_path, test_seg_path)
