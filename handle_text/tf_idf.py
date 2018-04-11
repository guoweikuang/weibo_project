# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
TF-IDF module

@author guoweikuang
"""
import jieba

from common.config import get_jieba_dict_path
from common.utils import load_stop_words
from sklearn.feature_extraction.text import CountVectorizer


jieba.load_userdict(get_jieba_dict_path("user_dict.txt"))


class TFIDF(object):
    """TF-IDF algorithm"""
    def __init__(self, rows):
        self.rows = rows
        self.stop_words = load_stop_words()
        self.seg_list = []

    def participle_text(self, text, word=7):
        """使用jieba对文本进行分词

        :return
        """
        seg_list = jieba.cut(text, cut_all=False)
        seg_content = set(seg_list) - self.stop_words
        if len(seg_content) >= word:
            return seg_content
        return

    def get_total_seg_content(self):
        """ 获取所有的文本分词后的集合 """
        for row in self.rows:
            seg = self.participle_text(row)
            if seg:
                self.seg_list.append(seg)
        return self.seg_list


