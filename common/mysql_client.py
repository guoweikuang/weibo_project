# -*- coding:utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
mysql client

  - save data to mysql

@author guoweikuang
"""
import pymysql
from DBUtils.PooledDB import PooledDB
from .config import Config
from .logger import logger
from .bloom_filter import is_repeat


class Client(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Client, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MysqlClient(object):
    def __init__(self, pool_num=5):
        self.pool_num = pool_num
        self.config = Config()
        self.pool = PooledDB(pymysql, self.pool_num,
                             host=self.config.host,
                             user=self.config.username,
                             passwd=self.config.password,
                             port=self.config.port,
                             db=self.config.db,
                             charset=self.config.charset)

        self.conn = self.pool.connection()
        self.cur = self.conn.cursor()

    def client(self):
        self.pool = PooledDB(pymysql, self.pool_num,
                             host=self.config.host,
                             user=self.config.username,
                             passwd=self.config.password,
                             port=self.config.port,
                             charset=self.config.charset)
        self.conn = self.pool.connection()
        self.cur = self.conn.cursor()
        return self.cur

    def save_data_to_mysql(self, *args, **kwargs):
        """save data to mysql

        :param args:
        :param kwargs:
        :return:
        """
        title, pub_time, comment_num, like_num, url = args
        try:
            sql = "INSERT INTO content(title, pub_time, comment_num, like_num, url) VALUES(%s, %s, %s, %s, %s);"
            if is_repeat(url):
                return
            self.cur.execute(sql, (title, str(pub_time), str(comment_num), str(like_num), url))
            self.conn.commit()

        except Exception as e:
            logger.error('mysql error: %s', e)
            self.conn.rollback()

    def close_mysql(self):
        self.conn.close()
        self.cur.close()
