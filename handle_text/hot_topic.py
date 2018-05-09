# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hot topic calculation

@author guoweikuang
"""
import re
import math
from collections import defaultdict
from common.redis_client import redis_client
from common.config import K_CLUSTER
from common.config import CLUSTER_RESULT
from common.config import HOT_CLUSTER
from common.config import EVERY_HOT_CLUSTER
from common.config import EVERY_TOP_KEYWORD
from handle_text.tf_idf import TFIDF
from .utils import get_categorys


class HotTopic(object):
    def __init__(self, db=1, hot_db=2):
        self.client = redis_client(db=db)
        self.hot_client = redis_client(db=hot_db)
        self.max_hot_value = {}

    def remove_hot_cache(self, category):
        for i in range(1, 15):
            keyword = '%s:%s' % (category, str(i))
            key_name = EVERY_HOT_CLUSTER % keyword
            if self.hot_client.exists(key_name):
                self.hot_client.delete(key_name)

    def remove_keyword_cache(self, category):
        for i in range(1, 15):
            key = "%s:%s" % (category, str(i))
            key_name = EVERY_TOP_KEYWORD % key
            if self.hot_client.hkeys(key_name):
                for keys in self.hot_client.hkeys(key_name):
                    self.hot_client.hdel(key_name, keys)

    def save_hot_to_redis(self, key_name, category, keyword_key):
        if self.client.llen(key_name):
            rows = self.client.lrange(key_name, 0, -1)
            rows = [row.decode('utf-8').split('\t') for row in rows]
            tf_idf = TFIDF(rows=rows)
            tf_dict = tf_idf.tf_idf()
            self.max_hot_value[key_name] = 0
            for row in rows:
                text, comment, like, pub_time = row
                self.max_hot_value[key_name] += float(comment) + float(math.sqrt(int(like)))
            if '学校新闻' in category:
                max_score = self.max_hot_value[key_name] * 2
            else:
                max_score = self.max_hot_value[key_name]
            self.hot_client.set(category, max_score)
            self.save_keywords_to_redis(keyword_key, tf_dict)

    def get_cluster_hot(self, k):
        """

        :param k:
        :return:
        """
        for i in range(1, k+1):
            key_name = CLUSTER_RESULT % (str(i))
            category_key = EVERY_HOT_CLUSTER % str(i)
            keyword_key = EVERY_TOP_KEYWORD % str(i)
            self.save_hot_to_redis(key_name, category_key, keyword_key)
        print(self.max_hot_value)
        hot_value = sorted(self.max_hot_value.items(), key=lambda d: d[1], reverse=True)
        for key, value in self.max_hot_value.items():
            self.save_max_hot_to_redis(key, value, "total")

    def get_first_cluster_hot(self, category):
        """ 获取第一次聚类后各类别热度值.

        :param category:
        :return:
        """
        fitst_key = "%s:cluster:1" % category
        if not self.client.llen(fitst_key):
            return
        self.remove_hot_cache(category)
        self.remove_keyword_cache(category)
        for i in range(1, 15):
            key_name = K_CLUSTER % (category, str(i))
            keyword = '%s:%s' % (category, str(i))
            category_key = EVERY_HOT_CLUSTER % keyword
            keyword_key = EVERY_TOP_KEYWORD % keyword
            self.save_hot_to_redis(key_name, category_key, keyword_key)
        hot_value = sorted(self.max_hot_value.items(), key=lambda d: d[1], reverse=True)
        print(hot_value)
        self.save_max_hot_to_redis(hot_value[0][0], hot_value[0][1], category)

    def get_second_cluster_hot(self, category):
        first_key = "%s:second:1" % category
        if not self.client.llen(CLUSTER_RESULT % first_key):
            return

        for i in range(1, 15):
            keyword = "%s:second:%s" % (category, str(i)) if category else str(i)
            key_name = CLUSTER_RESULT % keyword
            category_key = EVERY_HOT_CLUSTER % keyword
            keyword_key = EVERY_TOP_KEYWORD % keyword
            self.save_hot_to_redis(key_name, category_key, keyword_key)
        hot_values = sorted(self.max_hot_value.items(), key=lambda d: d[1], reverse=True)
        # print(hot_values)
        self.save_max_hot_to_redis(hot_values[0][0], hot_values[0][1], category)

    def create_or_remove(self, key_name):
        """

        :param key_name:
        :return:
        """
        if self.hot_client.llen(key_name):
            self.hot_client.delete(key_name)

    def save_max_hot_to_redis(self, hot_key, hot_values, category):
        max_key = hot_key.replace("cluster:", '').replace(":text", '')
        hot_key = HOT_CLUSTER % max_key
        if category == '学校新闻':
            hot_values = hot_values * 2
        #print(hot_values)
        #print(hot_key)
        #print(category)
        #self.hot_client.set(hot_key, hot_values)
        self.hot_client.set("cluster:%s:hot" % category, hot_values)

    def save_keywords_to_redis(self, key_name, tf_dict):
        """ save key to redis.

        :param tf_dict:
        :return:
        """
        if self.hot_client.hkeys(key_name):
            for keys in self.hot_client.hkeys(key_name):
                self.hot_client.hdel(key_name, keys)
        tf_dict = sorted(tf_dict.items(), key=lambda d: d[1], reverse=True)
        for key, value in tf_dict[:10]:
            self.hot_client.hset(key_name, key, value)


def get_max_hot_topic(db=1, hot_type='first'):
    """ 从redis中读取最大热度值的微博话题关键词.

    :param db:
    :return:
    """
    categorys = get_categorys()
    client = redis_client(db=db)
    hots = {}
    for category in categorys:
        category = category[:-4]
        key_name = HOT_CLUSTER % category
        value = client.get(key_name)
        hots[category] = float(value)

    result = sorted(hots.items(), key=lambda d: d[1], reverse=True)
    max_hot_category = result[0][0]
    max_hot_value = result[0][1]
    print(result)
    return max_hot_category, max_hot_value


def get_hot_keyword(db=1):
    """

    :param db:
    :param category:
    :return:
    """
    client = redis_client(db=db)
    category, hot_value = get_max_hot_topic(db=db)
    index = -1
    results = {}
    for i in range(1, 15):
        key = '%s:%s' % (category, str(i)) if db == 1 else "%s:second:%s" % (category, str(i))
        key_name = EVERY_HOT_CLUSTER % key
        if client.exists(key_name):
            value = client.get(key_name)
            results[str(i)] = float(value)
    results = sorted(results.items(), key=lambda d: d[1], reverse=True)
    print(results)
    index = int(results[0][0])
    key = "%s:%s" % (category, str(index) if index >= 1 else str(1)) if db == 1 else \
        "%s:second:%s" % (category, str(index))
    keywords = EVERY_TOP_KEYWORD % key
    if client.hkeys(keywords):
        results = client.hgetall(keywords)
        return results, index
    else:
        return {}, 1


def get_max_text(category, index, db=0):
    """

    :param db:
    :return:
    """
    client = redis_client(db=db)

    key_name = K_CLUSTER % (category, str(index))
    results = []

    if client.llen(key_name):
        results = client.lrange(key_name, 0, -1)

        results = [result.decode('utf-8') for result in results]

    return results


def list_hot_topic(db=1):
    """

    :return:
    """
    categorys = get_categorys()
    client = redis_client(db=db)
    result = {}

    for category in categorys:
        category = category[:-4]
        for i in range(1, 15):
            key = "%s:%s" % (category, str(i))
            key_name = EVERY_HOT_CLUSTER % key if db == 1 else EVERY_HOT_CLUSTER % ("%s:second:%s" % (category, str(i)))
            if client.exists(key_name):
                result[key_name] = float(client.get(key_name))
            else:
                break
    scores = sorted(result.items(), key=lambda d: d[1], reverse=True)[:8]
    sequence = []

    pattern = re.compile("category:(.*?):hot")
    for key, value in scores:
        key_name = re.search(pattern, key).group(1)
        keyword_name = EVERY_TOP_KEYWORD % key_name
        if client.hkeys(keyword_name):
            keywords = client.hgetall(keyword_name)
            keywords = sorted(keywords.items(), key=lambda d: d[1], reverse=True)
            words = [word.decode('utf-8') for word, value in keywords]
            key_text = ' '.join(words[:8])
            sequence.append([key_name, key_text, value])
    return sequence


def get_texts_from_redis(category, cate_num, db=0):
    """

    :param category:
    :param db:
    :return:
    """
    client = redis_client(db=db)
    key_name = K_CLUSTER % (category, str(cate_num)) if db == 0 else \
        CLUSTER_RESULT % ("%s:%s" % (category, str(cate_num)))
    result = []
    if client.llen(key_name):
        result = client.lrange(key_name, 0, -1)
    return result



