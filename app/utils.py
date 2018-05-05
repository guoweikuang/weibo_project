# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
handle something module


@author guoweikuang
"""
import re
import arrow
from collections import defaultdict
from pyecharts import Bar

from flask_admin import BaseView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from .auth.forms import AdminLoginForm

from common.mysql_client import get_mysql_client
from common.mysql_client import get_text_from_mysql
from handle_text.k_means import run_kmeans_by_scikit
from common.utils import classify_k_cluster_to_redis
from common.const import sensetive_dict
from utils import run_old_all_process
from handle_text.hot_topic import get_max_hot_topic
from handle_text.hot_topic import get_hot_keyword
from handle_text.hot_topic import get_max_text
from handle_text.hot_topic import list_hot_topic
from handle_text.hot_topic import get_texts_from_redis
from handle_text.draw_chart import run_get_hot_scores


class AdminView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = AdminLoginForm()
        if form.validate_on_submit():
            return self.render('admin/index.html', form=form)
        return self.render('admin/index.html', form=form)

    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_administator:
            return True
        return False


class UserView(ModelView):
    can_delete = False
    can_edit = False
    can_create = False

    column_labels = dict(
        username='用户名'
    )

    column_exclude_list = (
        'password_hash',
    )

    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_administator():
            return True
        return False


class ContentView(ModelView):
    can_delete = False
    can_edit = False
    can_create = False

    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_administator():
            return True
        return False


def filter_data(start_time, end_time, table_name="content"):
    """ filter weibo data from the specified time period.

    :param start_time: start date
    :param end_time:  end date
    :param table_name: data table name
    :return:
    """
    datas = get_text_from_mysql(table_name=table_name,
                                start_time=start_time,
                                end_time=end_time)
    return datas


def run_k_means(k, vsm_name='total'):
    """ k-means alogithrm.

    :param k: the cluster center numbers
    :param vsm_name: vsm name
    :return:
    """
    labels = run_kmeans_by_scikit(k, vsm_name=vsm_name)
    return labels


def classify_k_cluster(labels, datas):
    """ classify k cluster by labels.

    :param labels: text label
    :param datas:  all text data
    :return:
    """
    classify_k_cluster_to_redis(labels=labels, texts=datas)


def get_mysql_content(days=1):
    start_time = arrow.utcnow().shift(days=-days).date()
    end_time = arrow.utcnow().date()

    datas = get_text_from_mysql(table_name='content',
                                start_time=start_time,
                                end_time=end_time)
    return datas


def get_mysql_opinion():
    client = get_mysql_client()
    sql = "SELECT event_type, sen_word, weibo_text, pub_time, comment, like_num FROM opinion;"
    client.cur.execute(sql)
    rows = client.cur.fetchall()

    results = defaultdict(list)
    sensitive = list(sensetive_dict.keys())
    for row in rows:
        for sen in sensitive:
            if row[0] == sen:
                results[sen].append(row)

    return results


def get_max_hot_keyword_chart(db=1):
    category, hot_value = get_max_hot_topic(db=db)
    keywords, index = get_hot_keyword(db=db)
    img_name = "%s%s" % (category, str(index)) + '.png'
    results = get_max_text(category, index)
    return keywords, img_name, results, category


def get_max_text_from_mysql(category, index):
    """

    :param category:
    :param index:
    :return:
    """
    results = get_max_text(category, index)
    results = [result.split('\t') for result in results]
    return results


def list_top_hot_topic(db=1):
    """
    当前时间段的热点话题排行榜.
    :return:
    """
    sequence = list_hot_topic(db=db)
    result = []
    print(sequence)
    pattern = re.compile(r':(\d+)')
    for index, seq in enumerate(sequence):
        name = seq[0].split(':')[0]
        num = re.search(pattern, seq[0]).group(1)
        new_name = name + "第%s类" % (num)
        sequence[index].pop(0)
        sequence[index].insert(0, new_name)
    return sequence


def get_hot_text_from_category(category, db=0):
    pattern = re.compile(r"第(\d+)类")
    cate_num = re.search(pattern, category).group(1)
    name = category.split('第')
    key_name = name[0] if db == 0 else "%s:second" % name[0]
    print(key_name)
    results = get_texts_from_redis(key_name, cate_num, db=db)
    results = [res.decode('utf-8').split('\t') for res in results]
    return results


def bar_chart():
    keys, values = run_get_hot_scores(db=1)
    bar = Bar('聚类结果各类别的最大热度值')
    bar.add('最大热度值',
            keys, values, is_more_utils=True)
    return bar