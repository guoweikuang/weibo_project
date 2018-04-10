# -*- coding: utf-8 -*-
import os


WEIBO_LOGIN_KEY = "weibo:username:%s"
WEIBO_LOGIN_COOKIE = "weibo:username:%s:cookie"


class Config(object):
    """数据库连接配置"""
    username = os.getenv("username") or "root"
    password = os.getenv("password") or "2014081029"
    db = os.getenv("db") or "weibo_project"
    port = int(os.getenv("port", "3306")) or 3306
    charset = "utf8"
    host = os.getenv("host") or "localhost"