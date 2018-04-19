# -*- coding: utf-8 -*-
"""
main package init
    init buleprint instance

@author guoweikuang
"""
from flask import Blueprint


weibo = Blueprint('weibo', __name__)


from . import views
