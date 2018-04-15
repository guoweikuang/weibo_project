# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
init flask extensions and flask instance

@author guoweikuang
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import config
from crawl.crawl import run_async_crawl


db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app(config_name):
    """ 初始化flask

    :param config_name: 配置名
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)


    # register weibo buleprint to app instance
    from .weibo import weibo
    app.register_blueprint(weibo)

    # register auth blueprint to app instances
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    return app
