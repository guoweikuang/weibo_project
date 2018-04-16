# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~
weibo module form

@author guoweikuang
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms import DateField

from wtforms.validators import DataRequired
from wtforms.validators import Length


class CrawlForm(FlaskForm):
    """ crawl weibo form
    这里的start_time, end_time 目的是实现获取
    某段时间端内的微博内容.
    """
    # 输入框必须为"年-月-日"格式
    #start_time = DateField("起始日期", validators=[DataRequired()], format="%Y-%m-%d")
    #end_time = DateField("终止日期", validators=[DataRequired()], format="%Y-%m-%d")

    start_page = IntegerField("起始页数", validators=[DataRequired()])
    end_page = IntegerField("终止页数", validators=[DataRequired()])
    submit = SubmitField("点击爬取")


class AnalyzeForm(FlaskForm):
    """ weibo analyse module form.

    """
    start_time = DateField("起始日期", validators=[DataRequired()], format="%Y-%m-%d")
    end_time = DateField("起始日期", validators=[DataRequired()], format="%Y-%m-%d")
    k_cluster = IntegerField("设置簇心数", validators=[DataRequired(
                                                    message="请输入聚类的k值（就是聚成几类)")])
    submit = SubmitField("开始分析")
