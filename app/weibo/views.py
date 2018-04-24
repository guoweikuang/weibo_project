# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~
main module

#author guoweikuang
"""
from flask import render_template
from flask import redirect
from flask import url_for
from flask_login import login_required

from . import weibo
from .forms import CrawlForm
from .forms import AnalyzeForm
from app import run_async_crawl
from app import run_build_vsm
from ..utils import filter_data
from ..utils import run_k_means
from ..utils import classify_k_cluster
from ..utils import get_mysql_content


@weibo.route('/', methods=['GET', 'POST'])
def index():
    """ 首页 """
    return render_template('weibo/index.html')


@weibo.route('/crawl', methods=['GET', 'POST'])
@login_required
def crawl():
    """ 爬取模块 """
    crawl_form = CrawlForm()
    result = get_mysql_content(days=1)
    if crawl_form.validate_on_submit():
        result = run_async_crawl(start_page=crawl_form.start_page.data,
                                 end_page=crawl_form.end_page.data)
        return redirect(url_for('weibo.crawl'))
    return render_template('weibo/crawl.html', form=crawl_form, results=result)


@weibo.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    """ 聚类分析

    :return:
    """
    analyze_form = AnalyzeForm()
    if analyze_form.validate_on_submit():
        k = analyze_form.k_cluster.data
        datas = run_build_vsm(start_time=analyze_form.start_time.data,
                             end_time=analyze_form.end_time.data)
        labels = run_k_means(k=k)
        classify_k_cluster(labels=labels, datas=datas)
        # return redirect(url_for("weibo.show_data"))
    return render_template('weibo/analyze.html', form=analyze_form)