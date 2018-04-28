# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~
filter conditon

@author guoweikuang
"""
from common.config import FITLER_CONDITION


def is_seg_content_condition(seg_content):
    """ 过滤掉分词后不符合要求长度的文本.

    :param seg_content: 分词
    :param condition: 分词长度
    :return: True or False
    """
    if len(seg_content) < FITLER_CONDITION:
        return False
    return True