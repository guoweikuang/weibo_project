# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~
redis client module

@author guoweikuang
"""
import redis
from .config import WEIBO_LOGIN_COOKIE


class Client(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Client, cls).__new__(cls, *args, **kwargs)


class RedisClient(Client):
    def __init__(self, host="localhost", port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.redis = redis.Redis(connection_pool=self.pool)

    @property
    def get_data(self, key):
        return self.redis.get(key)

    def set_data(self, key, data):
        pass


def redis_client(host="localhost", port=6379, db=0):
    pool = redis.ConnectionPool(host=host, port=port, db=db)
    client = redis.Redis(connection_pool=pool)
    return client


class Cache(object):
    def __init__(self, name=WEIBO_LOGIN_COOKIE):
        self.name = name
        self.client = redis_client()

    def is_cookie_in_cache(self):
        """check if cookies exists in the cache

        :param name: cookie key name
        :return: True or False
        """
        if self.client.hkeys(self.name):
            return True
        else:
            return False

    def remove_cookie_from_cache(self, name=None):
        """remove if cookies exists in the cache

        :param name: cookie key name
        :return: None
        """
        if self.client.hkeys(self.name):
            keys = self.client.hkeys(self.name)
            self.client.hdel(self.name, keys)

    def save_cookie_to_cache(self, values=None):
        """saving cookie to cache

        :param values:
        :return: None
        """
        if self.client.hkeys(self.name):
            self.remove_cookie_from_cache()
        else:
            self.client.hmset(self.name, values)