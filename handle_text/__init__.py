# -*- coding: utf-8 -*-
import jieba
from common.config import get_jieba_dict_path

jieba.load_userdict(get_jieba_dict_path("user_dict.txt"))