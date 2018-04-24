# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
handle_text utils module

@author guoweikuang
"""
import os
import shutil
from common.config import abs_path
from common.config import VSM_NAME
from common.config import CLUSTER_RESULT
from common.redis_client import redis_client
from sklearn import metrics
from sklearn.cluster import KMeans


def load_data_set(vsm_name):
    """ load dataset from redis

    :param vsm_name: vsm name
    :return:
    """
    client = redis_client()

    datas = client.lrange(VSM_NAME % vsm_name, 0, -1)
    data_set = []
    for data in datas:
        data = [float(i) for i in data.decode('utf-8').strip().split(" ")]
        data_set.append(data)
    return data_set


def classify_k_cluster_to_redis(labels, texts, filename="cluster_result"):
    """ 对k-means 聚类后结果写入redis 或写入文本

    :param labels: 所有文本的label, 分类标志
    :param texts: 所有文本
    :return:
    """
    label_type = set(labels)
    client = redis_client()

    for label in label_type:
        key_name = CLUSTER_RESULT % str(label+1)
        if client.llen(key_name):
            client.delete(key_name)

    for label, rows in zip(labels, texts):
        key_name = CLUSTER_RESULT % str(label+1)
        title, pub_time, comment_num, like_num = rows
        text = title + '\t' + comment_num + '\t' + like_num + '\t' + pub_time
        client.lpush(key_name, text)


def classify_k_cluster_to_file(labels, texts, vsm_name="total", filename="cluster_result"):
    """ 对k-means 聚类后结果写入文本.

    :param labels: 所有文本的label, 分类标识
    :param texts:  所有文本内容
    :param filename: 文件名称
    :return:
    """
    key_name = VSM_NAME % vsm_name
    label_type = set(labels)
    vsms = get_vsm_from_redis(key_name)[::-1]
    is_cluster_file_exists(filename)
    #for label in label_type:
        #filename = "cluster_{}".format(label + 1)
        #is_cluster_file_exists(filename)

    for label, rows, vsm in zip(labels, texts, vsms):
        filename = "cluster_{}".format(label+1)
        vsm_path = os.path.join(abs_path, 'cluster_result/result/%s.txt' % filename)
        title, pub_time, comment_num, like_num = rows
        text = title.encode('utf-8') + '\t'.encode('utf-8') + comment_num.encode('utf-8') + '\t'.encode('utf-8') \
               + like_num.encode('utf-8') + '\t'.encode('utf-8') + pub_time.encode('utf-8') + '\n'.encode('utf-8')
        vsm = vsm.decode('utf-8').encode('utf-8')
        with open(vsm_path, 'ab') as fp:
            fp.write(text)
            fp.write(vsm + '\n'.encode('utf-8'))


def get_vsm_from_redis(vsm_name):
    """ 从redis获取vsm 值.

    :param vsm_name: vsm name
    :return:
    """
    client = redis_client()
    results = client.lrange(vsm_name, 0, -1)
    return results


def get_cluster_result(filename):
    """ 获取vsm 向量化后的文本

    :param filename: file name
    :return:
    """
    vsm_path = os.path.join(abs_path, 'cluster_result/result/%s.txt' % filename)


def is_cluster_file_exists(filename):
    """ 判断vsm 文本是否存在，若存在则删除，返回True,否则返回False.

    :param filename: file name
    :return: True or False
    """
    vsm_path = os.path.join(abs_path, 'cluster_result/result')
    if os.path.exists(vsm_path):
        shutil.rmtree(vsm_path)
        os.mkdir(vsm_path)
        return False
    if not os.path.exists(vsm_path):
        os.mkdir(vsm_path)
    return True


def set_cluster_result(filename, scores, texts):
    """ 把vsm 向量化后值和原始内容存入文本中.

    :param filename: vsm file name
    :param scores: 所有向量化后的值
    :param texts:  所有原始内容
    :return:
    """
    vsm_path = os.path.join(abs_path, 'cluster_result/result/%s.txt' % filename)
    is_cluster_file_exists(vsm_path)


def set_vsm_to_file(vsm_name, scores, texts):
    """ 把vsm 向量化后值和原始内容存入文本中.

    :param filename: vsm file name
    :param scores: 所有向量化后的值
    :param texts:  所有原始内容
    :return:
    """
    vsm_path = os.path.join(abs_path, 'cluster_result/vsm')
    if os.path.exists(vsm_path):
        shutil.rmtree(vsm_path)
        os.mkdir(vsm_path)

    if not os.path.exists(vsm_path):
        os.mkdir(vsm_path)

    filename = os.path.join(vsm_path, '%s.txt' % vsm_name)
    for score, text in zip(scores, texts):
        with open(filename, 'ab') as fp:
            fp.write(score.encode('utf-8') + '\n'.encode('utf-8'))
            #fp.write(text[0].encode('utf-8') + '\n'.encode('utf-8'))


def get_text_from_file(filename):
    """ 获取微博数据从文本中.

    :param filename:
    :return:
    """
    file_path = os.path.join(abs_path, 'cluster_result/data/%s.txt' % filename)
    result = []
    with open(file_path, 'rb') as fp:
        for line in fp.readlines():
            text, comment, like, date = line.decode('utf-8').split('\t')
            if len(text) >= 10 and int(like) >= 10:
                result.append(line)
            elif len(text) >= 10 and int(comment) >= 2:
                result.append(line)

    return result


def find_optimal_k_value(data_set):
    scores = {}
    for k in range(2, 13):
        cluster = KMeans(init='k-means++', n_clusters=k)
        matrix = cluster.fit_predict(data_set)
        scores[k] = metrics.calinski_harabaz_score(data_set, matrix)
    scores = sorted(scores.items(), key=lambda d: d[1], reverse=True)
    print(scores)
    return scores[0][0]