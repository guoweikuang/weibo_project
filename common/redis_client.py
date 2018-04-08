# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~
redis client module

@author guoweikuang
"""
import redis


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






