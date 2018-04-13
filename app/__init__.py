# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
init flask extensions and flask instance

@author guoweikuang
"""
from flask import Flask

from config import config


def create_app(config_name):
    """ 初始化flask

    :param config_name: 配置名
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
