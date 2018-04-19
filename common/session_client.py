# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
session module
    - session 状态保持
    - get cookie from redis

@author guoweikuang
"""
import requests
import grequests

from .utils import get_cookies_from_redis
from .utils import get_login_headers
from .utils import get_common_headers


session = requests.Session()
async_session = grequests.Session()


def session_client(mode="common", name=None):
    """构建session会话对象，保持登录状态

    :param mode: 登录模式，如果是login则切换不同headers
    :param return: session 对象
    """
    cookies = get_cookies_from_redis(name)
    headers = get_common_headers()
    if mode == "login":
        headers = get_login_headers()
    session.cookies.update(cookies)
    session.headers.update(headers)
    return session


def async_session_client(mode="common", name=None):
    """构建异步session会话对象，保持登录状态

    :param mode: 登录模式，如果是login则切换不同headers
    :param return: session 对象
    """
    cookies = get_cookies_from_redis(name)
    headers = get_common_headers()
    if mode == "login":
        headers = get_login_headers()
    async_session.cookies.update(cookies)
    async_session.headers.update(headers)
    return async_session
