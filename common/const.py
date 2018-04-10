# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
handle time

@author guoweikuang
"""


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


