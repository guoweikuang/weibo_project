# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~
utils module

@author guoweikuang
"""
import os
import arrow
import numpy
from datetime import date

from handle_text.build_vsm import BuildVSM
from handle_text.build_vsm import run_build_vsm_by_file
from handle_text.tf_idf import TFIDF
from handle_text.utils import get_text_from_file
from handle_text.utils import classify_k_cluster_to_file
from handle_text.utils import classify_k_cluster_to_redis
from handle_text.utils import save_k_cluster_to_redis
from handle_text.build_vsm import run_build_vsm
from handle_text.utils import classify_k_cluster_from_category
from handle_text.build_vsm import run_build_vsm_by_texts
from handle_text.k_means import run_kmeans_by_scikit
from handle_text.k_means import run_kmeans
from handle_text.utils import find_optimal_k_value
from common.config import abs_path
from common.config import K_CLUSTER
from common.utils import load_data_set
from common.redis_client import redis_client
from common.mysql_client import get_text_from_mysql
from handle_text.hot_topic import HotTopic
from handle_text.utils import get_categorys
from handle_text.draw_chart import run_draw_cluster_chart
from handle_text.draw_chart import run_keywrod_barh
from handle_text.draw_chart import run_draw_chart
from handle_text.draw_chart import run_draw_top_keyword_barh
from classify_text.utils import read_text_old_mysql, save_to_file
from classify_text.main import run_classify_text
from classify_text.classify import run_classify
from classify_text.config import corpus_path, seg_path, bag_path, test_bag_path, test_seg_path, test_corpus_path


def find_best_k_value(rows, category):
    """ 获取最优k值

    :param rows:
    :param category:
    :return:
    """
    k = 4
    if len(rows) <= 15:
        k = 1
    elif 15 < len(rows) < 30:
        k = 2
    return k


def run_first_cluster(start_time, end_time, k=1):
    """ 一次聚类并存入数据库.

    :param start_time:
    :param end_time:
    :param k:
    :return:
    """
    categories = os.listdir(os.path.join(abs_path, 'classify_text/data'))
    for category in categories:
        rows = get_text_from_file(category[:-4], cate='category')
        rows = [row.decode('utf-8').strip().split('\t') for row in rows]
        tf_idf = TFIDF(rows)
        tf_idf_dict = tf_idf.tf_idf()
        texts = tf_idf.get_filter_text()
        vsm = BuildVSM(tf_idf_dict, tf_idf.seg_list, texts, vsm_name=category[:-4])
        vsm.build_vsm()

        # 获取过滤后的文本
        rows = vsm.filter_text()
        data_set = numpy.mat(load_data_set(vsm_name=category[:-4]))
        k = find_optimal_k_value(data_set)
        print(category, k)
        #k = find_best_k_value(rows, category)
        print('k:', k)
        if k == 1:
            labels = [0] * len(data_set)
        else:
            labels = run_kmeans_by_scikit(k=k, vsm_name=category[:-4])
            #labels = run_kmeans(k=k, vsm_name=category[:-4])
        save_k_cluster_to_redis(labels=labels, texts=rows, category=category[:-4])
        classify_k_cluster_from_category(labels=labels, texts=rows, vsm_name=category[:-4], category=category[:-4])


def get_max_text_from_redis(category):
    """ 获取一次聚类后的最大数量的类.

    :param category:
    :return:
    """
    max_num = 0
    read_client = redis_client()
    max_key = K_CLUSTER % (category, 1)
    for i in range(1, 15):
        key_name = K_CLUSTER % (category, i)

        if read_client.llen(key_name) > max_num:
            max_num = read_client.llen(key_name)
            max_key = key_name

    rows = read_client.lrange(max_key, 0, -1)
    return rows[::-1]


def run_second_cluster():
    """ 二次聚类

    :param key_name:
    :return:
    """
    categories = get_categorys()

    for category in categories:
        results = get_max_text_from_redis(category[:-4])
        if not results:
            continue
        results = [row.decode('utf-8').split('\t') for row in results]
        if len(results) <= 30:
            k = 2
        else:
            k = 4
        vsm_name = category[:-4] + ':second'
        texts = run_build_vsm_by_texts(results, vsm_name=vsm_name)
        labels = run_kmeans_by_scikit(k=k, vsm_name=vsm_name)
        classify_k_cluster_to_redis(labels=labels, texts=texts, category=category[:-4], db=1)


def run_hot_topic(db=1, hot_db=2, hot_type="first"):
    """ 获取各分类热点话题热度值.

    :return:
    """
    categorys = get_categorys()

    for category in categorys:
        topic = HotTopic(db=db, hot_db=hot_db)
        category = category[:-4]
        if hot_type == 'first':
            topic.get_first_cluster_hot(category)
        else:
            topic.get_second_cluster_hot(category)


def run_first_cluster_hot_topic():
    """ 整个聚类过程包括热度计算等.

    :return:
    """
    # run_first_cluster('1', '1')
    run_hot_topic(db=0, hot_db=1)


def run_second_cluster_hot_topic(db=1, hot_db=2):
    """

    :param db:
    :param hot_db:
    :return:
    """
    run_hot_topic(db=db, hot_db=hot_db, hot_type='second')


def run_cluster(start, end, k=7):
    """ 旧数据库数据全套热点话题流程， test.

    :param start:
    :param end:
    :param k:
    :return:
    """
    #start = arrow.get(start, 'YYYY-MM-DD').date()
    #end = arrow.get(end, 'YYYY-MM-DD').date()
    end_time = arrow.get("2016-10-30")
    rows = read_text_old_mysql(end_time, days=20, database='weibo')

    #rows, texts = run_build_vsm(start_time=start, end_time=end)

    rows = run_build_vsm_by_texts(texts=rows, vsm_name='total')
    data_set = numpy.mat(load_data_set(vsm_name='total'))
    k = find_optimal_k_value(data_set)
    print(k)
    labels = run_kmeans_by_scikit(k=k, vsm_name="total")

    classify_k_cluster_to_file(labels=labels, texts=rows)
    classify_k_cluster_to_redis(labels=labels, texts=rows)

    topic = HotTopic(db=0, hot_db=1)
    topic.get_cluster_hot(k)

    run_draw_cluster_chart(db=1)
    run_keywrod_barh(db=1)


def run_all_process(start_time, end_time):
    """

    :param start_time:
    :param end_time:
    :return:
    """
    start = arrow.get(start_time, 'YYYY-MM-DD').date()
    end = arrow.get(end_time, 'YYYY-MM-DD').date()

    rows = get_text_from_mysql('content', start_time=start, end_time=end)
    run_classify_text(rows)
    run_first_cluster('1', '1')


def run_new_all_process(start_time, end_time, k):
    """ 新数据库热点话题发现流程. （一次聚类）

    :param start_time:
    :param end_time:
    :param k:
    :return:
    """
    if isinstance(start_time, date):
        start = start_time
    else:
        start = arrow.get(start_time, 'YYYY-MM-DD').date()
    if isinstance(end_time, date):
        end = end_time
    else:
        end = arrow.get(end_time, 'YYYY-MM-DD').date()

    rows = get_text_from_mysql('content', start_time=start, end_time=end)

    run_classify_text(rows)
    run_classify(corpus_path, seg_path, bag_path, test_bag_path, test_corpus_path, test_seg_path)

    run_first_cluster('1', '1')
    run_first_cluster_hot_topic()

    run_draw_chart(db=1)
    run_draw_top_keyword_barh(db=1)


def run_old_second_all_process(start_time, end_time):
    """
    所有流程汇总. test 使用
    :param start_time:
    :param end_time:
    :return:
    """
    rows = read_text_old_mysql(end_time, days=30, database='weibo')
    #save_to_file('old_mysql', rows)
    run_classify_text(rows)
    run_classify(corpus_path, seg_path, bag_path, test_bag_path, test_corpus_path, test_seg_path)
    run_first_cluster('1', '1')
    run_second_cluster()
    #run_hot_topic(db=1, hot_db=2)
    run_second_cluster_hot_topic(db=1, hot_db=2)
    run_draw_chart(db=2)
    run_draw_top_keyword_barh(db=2, draw_type='second')


def run_old_all_process(end_time):
    """

    :param end_time:
    :return:
    """
    rows = read_text_old_mysql(end_time, days=30, database='weibo')
    save_to_file('old_mysql', rows)

    # 分类并进行正确归类
    run_classify_text(rows)
    run_classify(corpus_path, seg_path, bag_path, test_bag_path, test_corpus_path, test_seg_path)

    run_first_cluster('1', '1')
    run_hot_topic(db=0, hot_db=1)
    run_draw_chart(db=1)
    run_draw_top_keyword_barh(db=1)

