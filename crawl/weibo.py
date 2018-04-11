# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
crawl weibo content

@author guoweikuang
"""
import re
from bs4 import BeautifulSoup

from common.session_client import session_client
from common.session_client import async_session_client
from common.utils import verify_response_status
from common.redis_client import Cache
from common.utils import filter_time
from common.const import EMOJI_PATTERN
from common.mysql_client import MysqlClient


class Spider(object):
    """crawl module"""
    def __init__(self, base_url, name, async=False):
        self.base_url = base_url
        self.name = name
        self.session = session_client(name=name) if not async else async_session_client(name=name)

    @verify_response_status(200)
    def get_response(self, page=1):
        url = self.base_url + "?page={}".format(page)
        response = self.session.get(url)
        #print(response.text)
        return response


class Parser(object):
    """提取微博文本"""
    def __init__(self, text):
        self.text = text
        self.result = []
        self.client = MysqlClient()

    def close_client(self):
        return self.client.close_mysql()

    def extract_text(self):
        """ 提取微博文本
        """
        soup = BeautifulSoup(self.text, 'lxml')
        for items in soup.find_all('div', class_='c', id=True):
            total = items.find_all('a')[::-1]
            nums = re.findall(r'\[(\d+)\]', str(total[1]))
            comment_num = int(nums[0])

            # 只提取有评论的微博文本
            if comment_num > 0:
                # 标题
                title = items.find('span', class_="ctt").get_text()
                title = self.extract_title(title)
                # 点赞数
                like = str(total[3])
                like = re.findall(r'\[(\d+)\]', like)
                like_num = int(like[0])
                # 发布时间
                pub_time = items.find('span', class_="ct")
                re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
                pub_time = re.sub(re_pattern, r'', pub_time.get_text().strip())
                pub_time = filter_time(pub_time)
                # url链接，用来去重
                url = items.find('a', class_="cc")
                url = url.get('href')
                print(comment_num, like_num, title, url)
                self.result.append((title, comment_num, like_num, url))
                self.client.save_data_to_mysql(title, pub_time, comment_num, like_num, url)

    def extract_title(self, title):
        """过滤内容中的特殊字符和表情

        :param title:
        :return:
        """
        title = title.replace('http://t.cn/Roeb5AN', '').replace("—发布端：", "").strip()
        try:
            result = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            result = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return result.sub(r"", title)
