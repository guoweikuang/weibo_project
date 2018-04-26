# -*- coding: utf-8 -*-
import os


WEIBO_LOGIN_KEY = "weibo:username:%s"
WEIBO_LOGIN_COOKIE = "weibo:username:%s:cookie"

# 向量空间 键名
VSM_NAME = "vsm:name:%s"

# 聚类结果存入redis 键名
CLUSTER_RESULT = "cluster:%s:text"

#
K_CLUSTER = "%s:cluster:%s"


# hot topic
HOT_CLUSTER = "cluster:%s:hot"

# every cluster hot
EVERY_HOT_CLUSTER = "category:%s:hot"


class Config(object):
    """数据库连接配置"""
    username = os.getenv("username") or "root"
    password = os.getenv("password") or "2014081029"
    db = os.getenv("db") or "weibo_project"
    port = int(os.getenv("port", "3306")) or 3306
    charset = "utf8"
    host = os.getenv("host") or "localhost"


abs_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DICT_PATH = os.path.join(abs_path, 'dict/user_dict.txt')


def get_jieba_dict_path(dict_name):
    """获取词表路径

    :param dict_name:
    :return:
    """
    PATH = os.path.join(abs_path, 'dict/%s' % dict_name)
    return PATH
