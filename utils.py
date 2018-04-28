# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~
utils module

@author guoweikuang
"""
import os
import arrow
import numpy

from handle_text.build_vsm import BuildVSM
from handle_text.build_vsm import run_build_vsm_by_file
from handle_text.tf_idf import TFIDF
from handle_text.utils import get_text_from_file
from handle_text.utils import classify_k_cluster_to_file
from handle_text.utils import classify_k_cluster_to_redis
from handle_text.utils import save_k_cluster_to_redis
from handle_text.utils import classify_k_cluster_from_category
from handle_text.build_vsm import run_build_vsm_by_texts
from handle_text.k_means import run_kmeans_by_scikit
from handle_text.utils import find_optimal_k_value
from common.config import abs_path
from common.config import K_CLUSTER
from common.utils import load_data_set
from common.redis_client import redis_client
from handle_text.hot_topic import HotTopic


def get_categorys():
    categorys = os.listdir(os.path.join(abs_path, 'classify_text/data'))
    return categorys


def run_first_cluster(start_time, end_time):
    categorys = os.listdir(os.path.join(abs_path, 'classify_text/data'))
    for category in categorys:
        rows = get_text_from_file(category[:-4], cate='category')
        rows = [row.decode('utf-8').strip().split('\t') for row in rows]
        #if len(rows) < 10:
        #    continue
        tf_idf = TFIDF(rows)
        tf_idf_dict = tf_idf.tf_idf()
        texts = tf_idf.get_filter_text()
        vsm = BuildVSM(tf_idf_dict, tf_idf.seg_list, texts, vsm_name=category[:-4])
        vsm.build_vsm()

        rows = vsm.filter_text()
        #data_set = numpy.mat(load_data_set(vsm_name=category[:-4]))
        # k = find_optimal_k_value(data_set)
        k = 4
        if category[:-4] == '校园生活':
            k = 2
        if len(rows) <= 5:
            k = 1
        if len(rows) <= 15:
            k = 1
        labels = run_kmeans_by_scikit(k=k, vsm_name=category[:-4])
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
    categorys = get_categorys()
    #read_client = redis_client()
    #write_client = redis_client(host='localhost', port=6379, db=1)

    for category in categorys:
        results = get_max_text_from_redis(category[:-4])
        if not results:
            continue
        results = [row.decode('utf-8').split('\t') for row in results]
        if len(results) <= 30:
            k = 2
        else:
            k = 3
        vsm_name = category[:-4] + ':second'
        texts = run_build_vsm_by_texts(results, vsm_name=vsm_name)
        labels = run_kmeans_by_scikit(k=k, vsm_name=vsm_name)
        classify_k_cluster_to_redis(labels=labels, texts=texts, category=category[:-4], db=1)


def run_hot_topic():
    """ 获取各分类热点话题热度值.

    :return:
    """
    categorys = get_categorys()

    for category in categorys:
        topic = HotTopic(db=1, hot_db=2)
        topic.get_second_cluster_hot(category[:-4])
