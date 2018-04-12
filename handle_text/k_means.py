# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~
K-Means module

@author guoweikuang
"""
import numpy


class KMeans(object):
    def __init__(self):
        pass

    def rand_cent(self, data_set, k):
        """
        :param data_set: 数据源，特征提取后的各文本特征权重集合
        :param k: 人工设定的聚类算法中心
        """
        n = numpy.shape(data_set)[1]  # 计算列数
        centroids = numpy.mat(numpy.zeros((k, n)))

        for j in range(n):
            min_j = min(data_set[:, j])  # 找出矩阵data_set每列最小值
            range__j = float(max(data_set[:, j]) - min_j)  # 计算第j列最大值和最小值的差
            # 赋予一个随机质心， 它的值在整个数据集的边界之内
            # random.rand(k,1)构建k行一列，每行代表二维的质心坐标
            centroids[:, j] = min_j + range__j * numpy.random.rand(k, 1)
        return centroids  # 返回一个随机的质心矩阵

    def euclidean_distance(vector1, vector2):
        """
        返回两个文本之间的距离
        :param vector1: 文本1的向量列表
        :param vector2:
        :return: 欧式距离
        """
        # return abs(vector1, vector2).max()
        return numpy.sqrt(sum(numpy.power(vector1 - vector2, 2)))

    def k_means(self, data_set, k, distance):
        """ kmeans algorthim

        :param data_set: 数据集
        :param k: k个簇心
        :param distance: 距离算法
        :return:
        """
        row = numpy.shape(data_set)[0]  # 获取行数

        # 初始化一个矩阵， 用来记录簇索引和存储误差平方和(指当前点到簇质点的距离）
        cluster_assment = numpy.mat(numpy.zeros((row, 2)))

        # 随机生成一个质心矩阵蔟
        centroids = self.rand_cent(data_set, k)
        cluster_change = True

        while cluster_change:
            cluster_change = False
            for i in range(row):  # 对每个数据点寻找最近的质心
                min_dist = numpy.inf  # 设置最小距离为正无穷大
                min_index = -1
                for j in range(k):  # 遍历质心簇，寻找最近质心
                    dist_j = distance(centroids[j, :], data_set[i, :])
                    if dist_j < min_dist:
                        min_dist = dist_j
                        min_index = j
                if cluster_assment[i, 0] != min_index:
                    cluster_change = True
                cluster_assment[i, :] = min_index, min_dist ** 2  # 平方的意义在于判断聚类结果的好坏

            for cent in range(k):  # 更新质心，将每个簇中的点的均值作为质心
                index_all = cluster_assment[:, 0].A  # 取出样本所属簇的索引值
                value = numpy.nonzero(index_all == cent)  # 取出所有属于第cent个簇的索引值
                sample_in_clust = data_set[value[0]]  # 取出属于第I个簇的所有样本点
                centroids[cent, :] = numpy.mean(sample_in_clust, axis=0)
        return centroids, cluster_assment