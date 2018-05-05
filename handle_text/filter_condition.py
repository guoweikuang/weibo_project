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


def filter_texts(texts):
    """
    过滤文本
    :param texts:
    :return:
    """
    result = []
    for text in texts:
        if len(text[0]) < 10 and int(text[2]) >= 5:
            result.append(text)
        elif len(text[0]) >= 10 and int(text[1]) >= 2:
            result.append(text)
    return result