# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
handle something module


@author guoweikuang
"""
import arrow
from collections import defaultdict

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