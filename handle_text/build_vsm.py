# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
text vector

@author guoweikuang
"""
from common.redis_client import redis_client
from common.config import VSM_NAME
from common.logger import logger
from common.mysql_client import get_text_from_mysql
from .tf_idf import TFIDF


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
        logger.info(tf_idf_list)
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
            self.redis_client.lpush(self.vsm_name, score_str)

    def remove_vsm_when_exists(self):
        if self.redis_client.llen(self.vsm_name):
            self.redis_client.ltrim(self.vsm_name, -1, 0)


def run_build_vsm(start_time, end_time):
    """
    构建向量空间模型
    :param start_time: datetime类型, 开始时间
    :param end_time:  datetime类型, 结束时间
    :return:
    """
    rows = get_text_from_mysql("content", start_time=start_time, end_time=end_time)
    from pprint import pprint
    pprint(rows)
    tf_idf = TFIDF(rows)
    tf_idf_dict = tf_idf.tf_idf()
    vsm = BuildVSM(tf_idf_dict, tf_idf.seg_list, vsm_name="total")
    vsm.build_vsm()
    return rows
