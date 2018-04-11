# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
TF-IDF module

@author guoweikuang
"""
import math
import jieba

from collections import Counter

from common.config import get_jieba_dict_path
from common.utils import load_stop_words
from common.utils import filter_title
from sklearn.feature_extraction.text import CountVectorizer


jieba.load_userdict(get_jieba_dict_path("user_dict.txt"))


class TFIDF(object):
    """TF-IDF algorithm"""
    def __init__(self, rows):
        self.rows = rows
        self.stop_words = load_stop_words()
        self.seg_list = []
        self.counter = Counter()
        self.tf_dict = {}
        self.tf_idf_dict = {}
        self.get_total_seg_content()

    def participle_text(self, text, word=7):
        """ 使用jieba对文本进行分词

        :return
        """
        text = filter_title(text)
        seg_list = jieba.cut(text, cut_all=False)
        seg_content = set(seg_list) - self.stop_words
        seg_content = list(seg_content)
        if len(seg_content) >= word:
            for word in seg_content:
                self.counter[word] += 1
            return seg_content
        return

    def get_total_seg_content(self):
        """ 获取所有的文本分词后的集合 """
        for row in self.rows:
            seg = self.participle_text(row[0])
            if seg:
                self.seg_list.append(seg)
        return self.seg_list

    def tf(self):
        """ tf algorithm
        计算所有关键词的tf值
        :return: dict, 所有关键词的tf值
        """
        words_num = len(self.counter)

        for word, value in self.counter.items():
            if value > 1:
                self.tf_dict[word] = float(value / words_num)

        return self.tf_dict

    def tf_idf(self):
        """ TF * IDF
        计算所有关键词的tf-idf权重值
        :return:
        """
        self.tf()
        print(self.counter)
        words_num = len(self.tf_dict)
        for word, value in self.tf_dict.items():
            self.tf_idf_dict[word] = float(value * float(math.log(words_num / value + 1)))

        return self.tf_idf_dict


