# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
text vector

@author guoweikuang
"""
from common.redis_client import redis_client
from common.config import VSM_NAME


class BuildVSM(object):
    def __init__(self, tf_idf_dict, seg_list, vsm_name="total"):
        """

        :param tf_idf_dict: 关键词权重表
        :param seg_list: 分词列表
        """
        self.tf_idf = tf_idf_dict
        self.seg_list = seg_list
        self.vsm_name = VSM_NAME % vsm_name
        self.redis_client = redis_client()

    def build_vsm(self):
        """ 构建空间向量模型VSM
        1 进行特征提取，目的是减少空间维度
        2 进行文本相似度对比
        """
        length = len(self.tf_idf)

        if length > 100:
            tf_idf_list = sorted(self.tf_idf.items(), key=lambda d: d[1], reverse=True)[:30]
        else:
            tf_idf_list = sorted(self.tf_idf.items(), key=lambda d: d[1], reverse=True)[:30]

        keywords = [word for word, _ in tf_idf_list]
        keywords_length = len(keywords)
        self.remove_vsm_when_exists()
        for words in self.seg_list:
            score = [0.0] * keywords_length
            unique_word = list(set(words) & set(keywords))  # 筛选出words中对应keywords中存在的关键词
            for word in unique_word:
                word_num = self.tf_idf.get(word, 0.0)
                index = keywords.index(word)
                score[index] = round(word_num, 3)
            if sum(score) == 0:
                continue
            score = map(str, score)
            score_str = ' '.join(score)
            #print(score_str)
            self.redis_client.lpush(self.vsm_name, score_str)

    def remove_vsm_when_exists(self):
        if self.redis_client.llen(self.vsm_name):
            self.redis_client.ltrim(self.vsm_name, -1, 0)
