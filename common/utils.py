# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~
need to handle somee

@author guoweikuang
"""
import re
import arrow
import requests
import random
from functools import wraps

from .redis_client import redis_client
from .config import WEIBO_LOGIN_COOKIE
from .const import DATE_MODE
from .const import DATE_PATTERN
from .const import DATETIME_PATTERN
from .const import TODAY_TIME
from .const import TODAY_PATTERN
from .const import MINUTES_BEFORE
from .const import MINUTES_PATTERN
from .const import URL_PATTERN
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
    cookies = redis_client().hgetall(WEIBO_LOGIN_COOKIE % name)
    cookies = {key.decode('utf-8'): value.decode('utf-8') for key, value in cookies.items()}
    return cookies

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


def filter_time(time_str):
    """ 提取时间

    :param time_str: time string
    :return: timestamp
    """
    utc = arrow.utcnow()
    if DATE_MODE in time_str:
        pattern = re.compile(DATE_PATTERN)
        result = re.search(pattern, time_str)
        month, day, hour, minute = map(int, result.groups())
        convert_time = utc.replace(month=month, day=day, hour=hour, minute=minute)

    elif MINUTES_BEFORE in time_str:
        pattern = re.compile(MINUTES_PATTERN)
        result = re.search(pattern, time_str)
        minute = int(result.group(1))
        convert_time = utc.replace(minute=minute)

    elif TODAY_TIME in time_str:
        pattern = re.compile(TODAY_PATTERN)
        result = re.search(pattern, time_str)
        hour, minute = map(int, result.groups())
        convert_time = utc.replace(hour=hour, minute=minute)

    else:
        pattern = re.compile(DATETIME_PATTERN)
        result = re.search(pattern, time_str)
        date = result.group(1)
        convert_time = arrow.get(date)

    return convert_time.datetime


def filter_url_mark(url):
    """提取url标识做为布隆过滤判断

    :param url:
    :return:
    """
    pattern = re.compile(URL_PATTERN)
    mark = re.search(pattern, url)
    return mark.group(1)
