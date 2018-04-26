# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~
K-Means module

@author guoweikuang
"""
import numpy
from common.utils import load_data_set
from sklearn.cluster import KMeans as K_Means
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import MeanShift
from .utils import find_optimal_k_value


class KMeans(object):
    def __init__(self, data_set, k):
        self.data_set = numpy.mat(data_set)
        self.k = k

    def rand_cent(self):
        """
        :param data_set: 数据源，特征提取后的各文本特征权重集合
        :param k: 人工设定的聚类算法中心
        """
        n = numpy.shape(self.data_set)[1]  # 计算列数
        centroids = numpy.mat(numpy.zeros((self.k, n)))

        for j in range(n):
            min_j = min(self.data_set[:, j])  # 找出矩阵data_set每列最小值
            range__j = float(max(self.data_set[:, j]) - min_j)  # 计算第j列最大值和最小值的差
            # 赋予一个随机质心， 它的值在整个数据集的边界之内
            # random.rand(k,1)构建k行一列，每行代表二维的质心坐标
            centroids[:, j] = min_j + range__j * numpy.random.rand(self.k, 1)
        return centroids  # 返回一个随机的质心矩阵

    def set_rand_cent(self):
        """ 人工设置簇心

        :return:
        """
        m = numpy.shape(self.data_set)[0]   # 行数
        n = numpy.shape(self.data_set)[1]   # 列数
        init_data = self.data_set[0, :]
        result = {}
        centroids = numpy.mat(numpy.zeros((self.k, n)))
        centroids[0, :] = init_data
        for j in range(1, self.k):
            distances = {}
            for i in range(1, n):
                distance = self.euclidean_distance(vector1=init_data, vector2=self.data_set[i, :])
                if i in result.keys():
                    continue
                distances[i] = distance
            index, max_distance = sorted(distances.items(), key=lambda d: d[1], reverse=True)[0]
            result[index] = max_distance
            centroids[j, :] = self.data_set[index, :]
            init_data = self.data_set[index, :]
        return numpy.mat(centroids)

    @staticmethod
    def euclidean_distance(vector1, vector2):
        """
        返回两个文本之间的距离
        :param vector1: 文本1的向量列表
        :param vector2:
        :return: 欧式距离
        """
        # return abs(vector1, vector2).max()
        distance = numpy.sqrt(numpy.sum(numpy.power(vector1 - vector2, 2)))
        return distance

    def person_distance(self, vector1, vector2):
        """
        : 距离算法
        :param vector1:
        :param vector2:
        :return:
        """
        sum1 = sum(vector1)
        sum2 = sum(vector2)

        sum1_sq = sum([pow(v, 2) for v in vector1])
        sum2_sq = sum([pow(v, 2) for v in vector2])

        p_sum = sum([vector1[i] * vector2[i] for i in range(vector1)])

        num = p_sum - sum1 * sum2 / len(vector1)
        den = numpy.sqrt((sum1_sq - pow(sum1, 2) / len(vector1)) * (sum2_sq - pow(sum2, 2)
                                                              / len(vector1)))
        if den == 0:
            return 0

        return 1.0 - num / den

    def k_means(self, distance=euclidean_distance):
        """ kmeans algorthim

        :param data_set: 数据集
        :param k: k个簇心
        :param distance: 距离算法
        :return:
        """
        row = numpy.shape(self.data_set)[0]  # 获取行数

        # 初始化一个矩阵， 用来记录簇索引和存储误差平方和(指当前点到簇质点的距离）
        cluster_assment = numpy.mat(numpy.zeros((row, 2)))

        # 随机生成一个质心矩阵蔟
        centroids = self.rand_cent()
        centroids = self.set_rand_cent()
        cluster_change = True

        while cluster_change:
            cluster_change = False
            for i in range(row):  # 对每个数据点寻找最近的质心
                min_dist = numpy.inf  # 设置最小距离为正无穷大
                min_index = -1
                for j in range(self.k):  # 遍历质心簇，寻找最近质心
                    dist_j = self.euclidean_distance(centroids[j, :], self.data_set[i, :])
                    if dist_j < min_dist:
                        min_dist = dist_j
                        min_index = j
                if cluster_assment[i, 0] != min_index:
                    cluster_change = True
                cluster_assment[i, :] = min_index, min_dist ** 2  # 平方的意义在于判断聚类结果的好坏

            for cent in range(self.k):  # 更新质心，将每个簇中的点的均值作为质心
                index_all = cluster_assment[:, 0].A  # 取出样本所属簇的索引值
                value = numpy.nonzero(index_all == cent)  # 取出所有属于第cent个簇的索引值
                sample_in_clust = self.data_set[value[0]]  # 取出属于第I个簇的所有样本点
                centroids[cent, :] = numpy.mean(sample_in_clust, axis=0)
        return centroids, cluster_assment


def run_kmeans(k, vsm_name="total"):
    """

    :param data_set:
    :return:
    """
    data_set = numpy.mat(load_data_set(vsm_name=vsm_name))
    k_means = KMeans(data_set, k)
    cluster_centroids, cluster_assment = k_means.k_means()
    # 获取矩阵中所有行的第一列,并生成每条文本所属的标签
    labels = cluster_assment[:, 0]
    labels = [int(i[0]) for i in labels.tolist()]
    print(labels)
    return labels


def run_kmeans_by_scikit(k, vsm_name="total"):
    """
    使用scikit-learn 库的kmeans算法
    :param k: 设置k个簇心
    :return:
    """
    
    data_set = numpy.mat(load_data_set(vsm_name=vsm_name))
    # k = find_optimal_k_value(data_set)
    k_means = K_Means(init="k-means++", n_clusters=k)
    matrix = k_means.fit_predict(data_set)
    labels = list(matrix)
    print(labels)
    return labels


def run_min_kmeans(k, vsm_name='total'):
    """
    使用scikit-learn 库的min means算法
    :param k: 设置k个簇心
    :return:
    """
    data_set = numpy.mat(load_data_set(vsm_name=vsm_name))
    k_means = MiniBatchKMeans(init="k-means++", n_clusters=k)
    matrix = k_means.fit_predict(data_set)
    labels = list(matrix)
    print(labels)
    return labels


def run_mean_shift(vsm_name='total'):
    """
    使用scikit-learn 库的mean shift算法
    :param k: 设置k个簇心
    :return:
    """
    data_set = numpy.mat(load_data_set(vsm_name=vsm_name))
    k_means = MeanShift()
    matrix = k_means.fit(data_set)
    labels = list(matrix.labels_)
    print(labels)
    return labels


def run_second_kmeans(k, vsm_name="vsm"):
    """ run k-means second.

    :param k:
    :param vsm_name:
    :return:
    """
    labels = run_kmeans_by_scikit(k, vsm_name=vsm_name)
    return labels
