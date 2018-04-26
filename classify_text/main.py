# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~
main module

@author guoweikuang
"""
import os
import shutil
import jieba
from .config import test_corpus_path
from .config import corpus_path
from .utils import load_stop_word
from .config import all_tag
from .config import word_tag


class Classify(object):
    def __init__(self, rows):
        self.rows = rows
        self.stop_list = load_stop_word()

    def create_or_exist(self, file_path):
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            os.mkdir(file_path)
        else:
            os.mkdir(file_path)

    def save_to_file(self, filename, category, content):
        """ save text to file.

        :param filename:
        :return:
        """
        file_path = os.path.join(corpus_path, category)
        full_path = os.path.join(file_path, '%s.txt' % filename)
        with open(full_path, 'wb') as fp:
            fp.write(content.encode('utf-8'))

    def classify_text(self):
        """ clssify text.

        :return:
        """
        for word in word_tag:
            category_path = os.path.join(corpus_path, word)
            self.create_or_exist(category_path)
        #self.create_or_exist(os.path.join(corpus_path, "毕业"))
        for index, row in enumerate(self.rows):
            if len(row[0]) < 10 and int(row[1]) < 1:
                continue
            seg_list = jieba.cut(row[0], cut_all=False)
            seg = [word for word in seg_list if word not in self.stop_list]

            for tag, name in zip(all_tag, word_tag):
                if len(set(tag) & set(seg)) != 0:
                    content = '\t'.join(row)
                    self.save_to_file(filename=index, category=name, content=content)


def run_classify_text(rows):
    """ 对文本进行分类.

    :param rows:
    :return:
    """
    print(rows)
    classify = Classify(rows=rows)
    classify.classify_text()