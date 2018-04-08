# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~
weibo login module

@author guoweikuang
"""
import requests
from common.utils import session
from common.utils import get_headers_from_random
from common.redis_client import redis_client
from common.config import WEIBO_LOGIN_COOKIE


class Login(object):
    """weibo login class"""

    def __init__(self, login_url, username, password):
        self.login_url = login_url
        self.username = username
        self.password = password
        self.client = redis_client()

    def login(self):
        """login method"""
        try:
            response = session.post(self.login_url, data=self.parser_data,
                                    headers=self.parser_header, timeout=5)
            if response.status_code == 200:
                self.client.hmset(WEIBO_LOGIN_COOKIE % self.username, session.cookies.get_dict())
        except requests.exceptions.ConnectTimeout:
            # TODO add log
            print('connect timeout')
        except requests.exceptions.Timeout:
            # TODO add log
            print("timeout")
        except Exception as e:
            print("error, ", e)

    @property
    def parser_data(self):
        post_data = {
            "username": self.username,
            "entry": "mweibo",
            "password": self.password,
            "mainpageflag": 1,
            "r": "http://weibo.cn/",
            "ec": 0
        }
        return post_data

    @property
    def parser_header(self):
        return get_headers_from_random()

