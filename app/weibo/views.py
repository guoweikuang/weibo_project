# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~
main module

#author guoweikuang
"""
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_login import login_required

from pyecharts import Bar
from pyecharts.utils import json_dumps
#from pyecharts import json_dumps
import json

from . import weibo
from .forms import CrawlForm
from .forms import AnalyzeForm
from app import run_async_crawl
from app import run_build_vsm
from ..utils import filter_data
from ..utils import run_k_means
from ..utils import classify_k_cluster
from ..utils import get_mysql_content
from ..utils import get_mysql_opinion
from ..utils import run_old_all_process
from ..utils import get_max_hot_keyword_chart
from ..utils import list_top_hot_topic
from ..utils import get_hot_text_from_category
from ..utils import bar_chart


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


@weibo.route('/', methods=['GET', 'POST'])
def index():
    """ 首页 """
    rows = list_top_hot_topic(db=1)
    category = request.values.get('topic')
    categorys = [cate[0] for cate in rows]
    results = []
    if category:
        categorys.remove(category)
        categorys.insert(0, category)
        results = get_hot_text_from_category(category, db=0)
    else:
        category = categorys[0]
        results = get_hot_text_from_category(category, db=0)
    print(results)
    return render_template('weibo/index.html', rows=rows, categorys=categorys, contents=results)


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
        run_old_all_process(start_time=analyze_form.start_time.data,
                            end_time=analyze_form.end_time.data,
                            k=analyze_form.k_cluster.data)
        #datas = run_build_vsm(start_time=analyze_form.start_time.data,
        #                     end_time=analyze_form.end_time.data)
        #labels = run_k_means(k=k)
        #classify_k_cluster(labels=labels, datas=datas)
        return redirect(url_for("weibo.display"))
    return render_template('weibo/analyze.html', form=analyze_form)


@weibo.route('/display', methods=['GET', 'POST'])
@login_required
def display():
    """ 图表展示.
    :return:
    """
    result = {}
    keywords, img_name, rows, category = get_max_hot_keyword_chart(db=1)
    name = "images/%s/%s" % (category, img_name)
    results = sorted(keywords.items(), key=lambda d: d[1], reverse=True)[::-1]
    keywords = [key.decode('utf-8') for key, value in results]
    rows = [row.split('\t') for row in rows]
    return render_template('weibo/display.html',
                           img_name=name,
                           keywords=keywords,
                           rows=rows)


@weibo.route('/sensitive', methods=['GET', 'POST'])
@login_required
def sensitive():
    """
    敏感词.
    :return:
    """
    results = get_mysql_opinion()
    opinion = ['心理健康', '社会突发事件', '校园安全', '反动言论']

    sen_type = request.values.get("category")
    if sen_type:
        opinion.remove(sen_type)
        opinion.insert(0, sen_type)
        rows = results[sen_type]
    else:
        rows = results[opinion[0]]

    return render_template('weibo/sensitive.html', rows=rows, categorys=opinion)


@weibo.route('/pyecharts', methods=['GET', 'POST'])
@login_required
def show_chart():
    """ test chart.

    :return:
    """
    bar = bar_chart()
    return render_template('pyecharts.html',
                           chart_id=bar.chart_id,
                           host=REMOTE_HOST,
                           my_width='100%',
                           my_height=600,
                           my_option=json_dumps(bar.options),
                           script_list=bar.get_js_dependencies())


