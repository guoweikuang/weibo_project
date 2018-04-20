# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
classify text config module

@author guoweikuang
"""
import os


abs_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

stop_path = os.path.join(parent_path, 'dict/user_stop_dict.txt')


corpus_path = os.path.join(abs_path, 'train_corpus')
seg_path = os.path.join(abs_path, 'train_seg')
bag_path = os.path.join(abs_path, 'train_bag')
test_bag_path = os.path.join(abs_path, 'test_bag')


test_corpus_path = os.path.join(abs_path, 'test_corpus')
test_seg_path = os.path.join(abs_path, 'test_seg')
