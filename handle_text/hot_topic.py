# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hot topic calculation

@author guoweikuang
"""
import math
from common.redis_client import redis_client
from common.config import K_CLUSTER
from common.config import CLUSTER_RESULT
from common.config import HOT_CLUSTER
from common.config import EVERY_HOT_CLUSTER
from handle_text.tf_idf import TFIDF


class HotTopic(object):
    def __init__(self, db=1, hot_db=2):
        self.client = redis_client(db=db)
        self.hot_client = redis_client(db=hot_db)

    def get_second_cluster_hot(self, category):
        first_key = "%s:second:1" % category
        if not self.client.llen(CLUSTER_RESULT % first_key):
            return

        max_hot_value = {}
        for i in range(1, 15):
            keyword = "%s:second:%s" % (category, str(i)) if category else str(i)
            key_name = CLUSTER_RESULT % keyword
            category_key = EVERY_HOT_CLUSTER % keyword
            if self.client.llen(key_name):
                self.create_or_remove(key_name)
                rows = self.client.lrange(key_name, 0, -1)
                rows = [row.decode('utf-8') for row in rows]
                tf_idf = TFIDF(rows)
                tf_dict = tf_idf.tf_idf()
                max_hot_value[key_name] = 0
                for row in rows:
                    text, comment, like, pub_time = row.strip().split('\t')
                    max_hot_value[key_name] += float(comment) + float(math.sqrt(int(like)))
                self.hot_client.set(category_key, max_hot_value[key_name])
        hot_values = sorted(max_hot_value.items(), key=lambda d: d[1], reverse=True)
        print(hot_values)
        max_hot = hot_values[0][0]
        hot_key = HOT_CLUSTER % (category)
        self.hot_client.set(hot_key, hot_values[0][1])

    def create_or_remove(self, key_name):
        """

        :param key_name:
        :return:
        """
        if self.hot_client.llen(key_name):
            self.hot_client.delete(key_name)

    def save_keywords_to_redis(self, tf_dict):
        """ save key to redis.

        :param tf_dict:
        :return:
        """
