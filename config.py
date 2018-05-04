# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
flask web cofig module

@author guoweikuang
"""
import os
from const import MYSQL_URL

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ common config """
    SECRET_KEY = 'GUO wei kuang blog'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    WEIBO_ADMIN = '673411814@qq.com'
    WEIBO_MAIL_SUBJECT_PREFIX = '[Guoweikuang]'
    WEIBO_MAIL_SENDER = '郭伟匡<15602200534@163.com>'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '15602200534@163.com'
    MAIL_PASSWORD = ''
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    USERNAME = os.environ.get("WEIBO_USERNAME") or "root"
    PASSWORD = os.environ.get("WEIBO_PASSWORD") or "2014081029"
    MYSQL_URL = MYSQL_URL.format(username=USERNAME, password=PASSWORD)
    #CELERY_BROKER_URL = 'redis://localhost:6379',
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ development config """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or MYSQL_URL


class TestingConfig(Config):
    """ test environment config
    need to set debug to True
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or MYSQL_URL


class ProductionConfig(Config):
    """ pruduction environment config
    need to set debug to False.

    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRO_DATABASE_URI") or MYSQL_URL


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,  # default to using development config
}
