# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~
classify text utils module

@author guoweikuang
"""
import os
import re
import arrow
import pickle
import pymysql
from .config import stop_path
from .config import FILENAME_PATTERN

from common.config import abs_path


def read_file(path):
    """ read file.

    :param path: file path
    :return:
    """
    content = None
    with open(path, 'rb') as fp:
        content = fp.read().decode('utf-8')
        content = content.replace('\r\n', '').strip()
    return content


def save_file(path, content):
    """ save file.

    :param path: file path
    :param content: save content
    :return:
    """
    with open(path, 'wb') as fp:
        fp.write(content)


def read_bunch(path):
    """ read bunch.

    :param path:
    :return:
    """
    file = open(path, 'rb')
    bunch = pickle.load(file)
    file.close()
    return bunch


def save_bunch(path, content):
    """ save bunch

    :param path:
    :return:
    """
    file = open(path, 'wb')
    pickle.dump(content, file)
    file.close()


def load_stop_word():
    stop_list = read_file(stop_path).splitlines()
    return stop_list


def remove_and_restart_join(corpus_path, error_path, expect_type, error_type):
    """ remove error type and restart join.

    :param file_name:
    :param expect_type:
    :return:
    """
    pattern = re.compile(FILENAME_PATTERN)
    file_name = re.search(pattern, error_path).group(1)
    error = os.path.join(corpus_path, error_type)
    full_error_path = os.path.join(error, '%s.txt' % file_name)
    with open(full_error_path, 'rb') as fp:
        content = fp.read()

    error_corpus_path = os.path.join(corpus_path, error_type)
    full_error_path = os.path.join(error_corpus_path, '%s.txt' % file_name)
    os.remove(error_path)
    os.remove(full_error_path)

    category_path = os.path.join(corpus_path, expect_type)
    full_path = os.path.join(category_path, '%s.txt' % file_name)
    with open(full_path, 'wb') as fp:
        fp.write(content)

    #error_corpus_path = os.path.join(corpus_path, error_type)
    #full_error_path = os.path.join(error_corpus_path, '%s.txt' % file_name)
    #os.remove(error_path)
    #os.remove(full_error_path)


def create_is_exists(path):
    """

    :param path:
    :return:
    """
    if os.path.exists(path):
        os.remove(path)


def classify_result(path, result_path):
    """ 把test_seg 各分类汇总.

    :param path:
    :return:
    """
    categorys = os.listdir(path)

    for category in categorys:
        category_path = os.path.join(path, category)
        file_path = os.path.join(result_path, '%s.txt' % category)
        create_is_exists(file_path)
        for file in os.listdir(category_path):
            full_file = os.path.join(category_path, file)
            with open(full_file, 'rb') as fp:
                content = fp.read()
            with open(file_path, 'ab') as fp:
                fp.write(content + '\n'.encode('utf-8'))


def use_mysql(database="weibo"):
    """

    :param database:
    :return:
    """
    conn = pymysql.connect(host='localhost',
                           user='root',
                           passwd='2014081029',
                           db=database,
                           charset='utf8')
    cur = conn.cursor()
    return conn, cur


def read_text_old_mysql(end_time, days, database="weibo"):
    """ 读取数据从旧数据库

    :param database:
    :return:
    """
    conn, cur = use_mysql(database=database)
    sql = "select * from content;"
    cur.execute(sql)
    rows = cur.fetchall()

    result = []
    start_time = end_time.shift(days=-days)
    for row in rows:
        pub_time = arrow.get(row[2], 'YYYY-MM-DD')
        pub_timestamp = pub_time.timestamp

        if start_time.timestamp <= pub_timestamp <= end_time.timestamp and len(row[1]) >= 10:
            temp = [row[1], row[4], row[5], row[2]]
            result.append(temp)
    return result


def save_to_file(file_name, rows):
    """ 保存数据到文本中，test使用.

    :param file_name:
    :param rows:
    :return:
    """
    file_path = os.path.join(abs_path, 'cluster_result/data/%s.txt' % file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'ab') as fp:
        for row in rows:
            text = '\t'.encode('utf-8').join([i.encode('utf-8') for i in row]) + '\n'.encode('utf-8')
            fp.write(text)
