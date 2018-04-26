# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~
error handler

@author guoweikuang
"""
from flask import render_template
from . import weibo


@weibo.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@weibo.app_errorhandler(401)
def forbidden(e):
    return render_template('403.html'), 401


@weibo.app_errorhandler(500)
def interanl_server_error(e):
    return render_template('500.html'), 500