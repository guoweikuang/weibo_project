# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~
classify text utils module

@author guoweikuang
"""
import os
import re
import pickle
from .config import stop_path
from .config import FILENAME_PATTERN


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
