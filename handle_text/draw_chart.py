# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
Drawing chart

@author guoweikuang
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from common.redis_client import redis_client
from common.config import HOT_CLUSTER
from common.config import EVERY_TOP_KEYWORD
from common.config import EVERY_HOT_CLUSTER
from common.config import CLUSTER_RESULT
from common.config import get_picture_path
from common.mysql_client import get_mysql_client
from common.const import sensetive_dict
from .utils import get_categorys



matplotlib.matplotlib_fname()
plt.rcParams['font.sans-serif'] = ['YaHei Consolas Hybrid']
plt.rcParams['axes.unicode_minus'] = False


class DrawChart(object):
    def __init__(self, db=2):
        self.db = db
        self.client = redis_client(db=self.db)
        self.mysql_client = get_mysql_client()
        self.categorys = get_categorys()
        self.hot_score = {}

    def get_category_hot_score(self):
        """ 获取所有分类的热度值.

        :return:
        """
        for category in self.categorys:
            category = category[:-4]
            key_name = HOT_CLUSTER % category
            score = self.client.get(key_name)
            if score:
                self.hot_score[category] = float(score)

    def get_hot_score(self):
        for i in range(1, 15):
            key_name = HOT_CLUSTER % str(i)
            score = self.client.get(key_name)
            if score:
                key = "第%s类" % str(i)
                self.hot_score[key] = float(score)

    def draw_category_histogram(self):
        scores = sorted(self.hot_score.items(), key=lambda d: d[1])
        print(scores)
        keys = [key[0] for key in scores]
        values = [key[1] for key in scores]
        length = len(keys)
        ind = np.arange(length)
        hot_values = tuple(values)
        x_labels = keys
        fig, axes = plt.subplots(1, 1)
        rects = axes.bar(ind, hot_values, width=0.35, color='rgby', align='center', yerr=0.00000001)
        axes.set_ylabel(u'最大热度值')
        axes.set_title(u'聚类结果各类别的最大热度值')
        axes.set_xticks(ind)
        axes.set_xticklabels(x_labels)

        for rect in rects:
            height = rect.get_height()
            axes.text(rect.get_x() + rect.get_width() / 2, 1.01 * height,
                      '%.2f' % float(height), ha='center', va='bottom')

        picture_path = get_picture_path()
        #plt.show()
        plt.savefig(os.path.join(picture_path, 'hot.png'))

    def get_top_keyword(self, category, i):
        key = "%s:second:%s" % (category, str(i)) if category else str(i)
        key_name = EVERY_TOP_KEYWORD % key
        if self.client.hkeys(key_name):
            result = self.client.hgetall(key_name)
            return result
        else:
            return {}

    def get_first_keyword(self, category, i):
        key = "%s:%s" % (category, str(i))
        key_name = EVERY_TOP_KEYWORD % key
        if self.client.hkeys(key_name):
            result = self.client.hgetall(key_name)
            return result
        else:
            return {}

    def draw_category_keyword(self, category, draw_type="first"):
        for i in range(1, 15):
            if draw_type == 'first':
                keywords = self.get_first_keyword(category, i)
            else:
                keywords = self.get_top_keyword(category, i)
            keywords = sorted(keywords.items(), key=lambda d: d[1], reverse=True)
            keys = [key[0] for key in keywords]
            values = [value[1] for value in keywords]
            if keywords:
                self.draw_top_keyword_barh(category + str(i), keys, values)

    def draw_top_keyword_barh(self, category, keys, values):
        """ draw top keyword barh.

        :param category:
        :param keys:
        :param values:
        :return:
        """
        plt.cla()
        length = len(keys)
        ind = np.arange(length)
        values = [float(value) for value in values]
        keys = [key.decode('utf-8') for key in keys]
        #print(values)
        plt.barh(ind, values, align='center', alpha=0.4, color='blue')
        #plt.xticks(ind, keys)
        plt.yticks(ind, keys)

        for y, value in zip(ind, values):
            value = round(value, 2)
            plt.text(value+0.025, y, value, ha='center', va='center', weight='bold')
        max_value = max(values)
        plt.xlim(0, max_value + 0.1)
        plt.xlabel(u'关键词权重')
        plt.title(u'%s 类别下关键词TOP10图' % category)
        picture_path = get_picture_path()
        #plt.show()
        plt.savefig(os.path.join(picture_path, '%s.png' % category))

    def draw_pie(self):
        plt.figure(figsize=(9, 6))
        labels = ["社会突发事件", '校园安全', '心理健康']
        percents = {}
        for label in labels:
            percents[label] = self.get_labels_percent(label)
        total = sum(percents.values())
        results = {}
        for key, value in percents.items():
            results[key] = round(value / float(total) * 100, 2)
        colors = ['red', 'yellowgreen', 'lightskyblue']
        labels = []
        scores = []
        for key, value in results.items():
            labels.append(key)
            scores.append(value)

        explode = (0.01, 0.01, 0.005)
        patches, l_text, p_text = plt.pie(scores, explode=explode, labels=labels, colors=colors,
                                          labeldistance=1.1, autopct='%3.1f%%', shadow=False,
                                          startangle=90, pctdistance=0.6)
        for t in l_text:
            t.set_size = (30)
        for t in p_text:
            t.set_size = (20)
        # 设置x，y轴刻度一致，这样饼图才能是圆的
        plt.axis('equal')
        plt.legend()
        picture_path = get_picture_path()
        plt.savefig(os.path.join(picture_path, 'sensitive.png'))
        plt.show()

    def get_labels_percent(self, label):
        sql = "SELECT count(*) from opinion where event_type = %s"
        self.mysql_client.cur.execute(sql, (label,))
        count = self.mysql_client.cur.fetchall()
        return int(count[0][0])


def run_draw_chart(db=2):
    """ run draw chart.

    :param db:
    :return:
    """
    draw = DrawChart(db=db)
    draw.get_category_hot_score()
    draw.draw_category_histogram()


def run_draw_cluster_chart(db=1):
    draw = DrawChart(db=db)
    draw.get_hot_score()
    draw.draw_category_histogram()


def run_draw_pie(db=2):
    draw = DrawChart(db=db)
    draw.draw_pie()


def run_draw_top_keyword_barh(db=2):
    """ draw top keyword barh.

    :param db:
    :return:
    """
    draw = DrawChart(db=db)
    categorys = get_categorys()

    for category in categorys:
        draw.draw_category_keyword(category[:-4], draw_type='first')


def run_keywrod_barh(db=1):
    """ 无分类条件下画图

    :param db:
    :return:
    """
    draw = DrawChart(db=db)
    draw.draw_category_keyword('')


def run_get_hot_scores(db=1):
    draw = DrawChart(db=db)
    draw.get_category_hot_score()

    hot_scores = draw.hot_score
    scores = sorted(hot_scores.items(), key=lambda d: d[1])
    keys = [key[0] for key in scores]
    values = [key[1] for key in scores]
    return keys, values
