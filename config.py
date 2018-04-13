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
    USERNAME = os.environ.get("USERNAME") or ""
    PASSWORD = os.environ.get("PASSWORD") or ""

    CELERY_BROKER_URL = 'redis://localhost:6379',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'

    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ development config """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = MYSQL_URL % (self.USERNAME, self.PASSWORD) or os.environ.get("DEV_DATAABSE_URI")


class TestingConfig(Config):
    """ test environment config
    need to set debug to True
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = MYSQL_URL % (self.USERNAME, self.PASSWORD) or os.environ.get("TEST_DATABASE_URI")


class ProductionConfig(Config):
    """ pruduction environment config
    need to set debug to False.

    """
    DEBUG = Flase
    SQLALCHEMY_DATABASE_URI = MYSQL_URL % (self.USERNAME, self.PASSWORD) or os.environ.get("PRO_DATABASE_URI")


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
