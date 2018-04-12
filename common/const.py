# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
handle time

@author guoweikuang
"""
import re

# XXX分钟前 形式
MINUTES_BEFORE = "分钟前"
MINUTES_PATTERN = "(\d+)分钟前"

# 今天 19:41 形式
TODAY_TIME = "今天"
TODAY_PATTERN = "今天 (\d+):(\d+)"

# 07月03日 11:23:23 形式
DATE_MODE = "月"
DATE_PATTERN = "(\d{2})月(\d{2})日 (\d{2}):(\d{2})"

# 2017-10-24 10:23:43 形式
DATETIME_PATTERN = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"


# 提取微博url 进行判重
URL_PATTERN = r"comment\/(\w+)\?uid"


# 表情
EMOJI_PATTERN = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)


# 过滤电话号码
NUMBER_PATTERN = re.compile(r"\d{11}")
