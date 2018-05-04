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
data_path = os.path.join(abs_path, 'data')


corpus_path = os.path.join(abs_path, 'train_corpus')
seg_path = os.path.join(abs_path, 'train_seg')
bag_path = os.path.join(abs_path, 'train_bag')
test_bag_path = os.path.join(abs_path, 'test_bag')


test_corpus_path = os.path.join(abs_path, 'test_corpus')
test_seg_path = os.path.join(abs_path, 'test_seg')

word_tag = ['买卖交易', '求助', '校园生活', '学校新闻', '网络', '情感', '毕业']
market_tag = ['评论', '私聊', '价格', '小刀', '有意', '有意者', '出售']
help_tag = ['请问', '有人', '谢谢', '求问']
campus_tag = ['同学', '宿舍', '毕业', '师兄', '图书馆', '考研', '考试', '宿友', '一卡通', '空调', '外卖']
college_tag = ['学院', '老师', '校区', '学校', '领导', '管理', '奖学金', '助学金']
network_tag = ['锐捷', '网卡', '报修', '二次认证', '断网', '网络中心']
emotion_tag = ['喜欢', '女朋友', '男朋友', '女生', '男生', '男票', '分手', '相亲', '恋爱', '脱单', '表白', '女票', '失恋']
graduate_tag = ['毕业生',  '毕业', '毕业照', '实习', '论文', '答辩', '工作', '招聘会', '简历', '薪水', '面试', '考研']

all_tag = [market_tag, help_tag, campus_tag, college_tag, network_tag, emotion_tag, graduate_tag]


# filter filename
FILENAME_PATTERN = r"\/(\d+).txt"