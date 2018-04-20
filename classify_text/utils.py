# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~
classify text utils module

@author guoweikuang
"""
import os
import pickle


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