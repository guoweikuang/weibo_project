# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
session module
    - session 状态保持
    - get cookie from redis

@author guoweikuang
"""
import requests

from .utils import get_cookies_from_redis
from .utils import get_headers_from_random


session = requests.Session()


def session_client():
    """构建session会话对象，保持登录状态"""
    cookies = get_cookies_from_redis()
    headers = get_headers_from_random()
    session.cookies.update(cookies)
    session.cookies.update(headers)
    return session