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
from .forms import CrawlForm
from app import run_async_crawl


@weibo.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """ 首页 """
    return render_template('weibo/index.html')


@weibo.route('/crawl', methods=['GET', 'POST'])
@login_required
def crawl():
    """ 爬取模块 """
    crawl_form = CrawlForm()
    if crawl_form.validate_on_submit():
        run_async_crawl(start_page=crawl_form.start_page.data,
                        end_page=crawl_form.end_page.data)
    return render_template('weibo/crawl.html', form=crawl_form)