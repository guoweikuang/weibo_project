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
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from config import config

from crawl.crawl import run_async_crawl
from handle_text.build_vsm import run_build_vsm


db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
admin = Admin(name='微博舆情监控后台')
babel = Babel()


from .models import User
from .utils import UserView
from .utils import AdminView


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
    babel.init_app(app)

    admin.init_app(app)
    #admin.add_view(AdminView(name='微博'))
    #admin.add_view(ModelView(User, db.session))
    admin.add_view(UserView(User, db.session, name='用户信息'))

    # register weibo buleprint to app instance
    from .weibo import weibo
    app.register_blueprint(weibo)

    # register auth blueprint to app instances
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    return app
