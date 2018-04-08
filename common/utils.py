# -*- coding: utf-8 -*-
import requests


session = requests.Session()


def get_headers_from_random():
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0",
        "Origin": "https://passport.weibo.cn",
        "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
    }
    return headers
