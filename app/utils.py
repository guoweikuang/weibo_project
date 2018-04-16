# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
handle something module


@author guoweikuang
"""
from common.mysql_client import get_mysql_client
from common.mysql_client import get_text_from_mysql
from handle_text.k_means import run_kmeans_by_scikit
from common.utils import classify_k_cluster_to_redis


def filter_data(start_time, end_time, table_name="content"):
    """ filter weibo data from the specified time period.

    :param start_time: start date
    :param end_time:  end date
    :param table_name: data table name
    :return:
    """
    datas = get_text_from_mysql(table_name=table_name,
                                start_time=start_time,
                                end_time=end_time)
    return datas


def run_k_means(k, vsm_name='total'):
    """ k-means alogithrm.

    :param k: the cluster center numbers
    :param vsm_name: vsm name
    :return:
    """
    labels = run_kmeans_by_scikit(k, vsm_name=vsm_name)
    return labels


def classify_k_cluster(labels, datas):
    """ classify k cluster by labels.

    :param labels: text label
    :param datas:  all text data
    :return:
    """
    classify_k_cluster_to_redis(labels=labels, texts=datas)