# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~
main module

#author guoweikuang
"""
from flask import render_template
from flask import redirect
from flask_login import login_required
from . import weibo


@weibo.route('/', method=['GET', 'POST'])
@login_required
def index():
    pass
