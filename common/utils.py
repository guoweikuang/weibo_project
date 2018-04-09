# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~
need to handle somee

@author guoweikuang
"""
import random
import requests
from functools import wraps

from .redis_client import redis_client
from .config import WEIBO_LOGIN_COOKIE
from .logger import logger


session = requests.Session()


# User-Agent list
USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
]


def get_agent_from_random():
    return random.choice(USER_AGENT_LIST)


def get_login_headers():
    headers = {
        'User-Agent': get_agent_from_random(),
        "Origin": "https://passport.weibo.cn",
        "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
    }
    return headers


def get_common_headers():
    headers = {
        'User-Agent': get_agent_from_random(),
        #"Referer": "https://weibo.cn/gzyhl",
    }
    return headers


def get_cookies_from_redis(name):
    """get cookies from redis
    """
    return redis_client().hgetall(WEIBO_LOGIN_COOKIE % name)


def verify_response_status(status_code):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                if response.status_code == status_code:
                    logger.info(response.status_code)
                    return response
                else:
                    return None
            except requests.exceptions.ConnectTimeout:
                # TODO ADD LOG
                logger.error("connect timeout")
                return None
            except requests.exceptions.Timeout:
                # TODO ADD LOG
                logger.error("timeout")
                return None
            except Exception as e:
                # TODO ADD LOG
                logger.error("error, %s" % e)
                return None
        return decorated
    return decorator
