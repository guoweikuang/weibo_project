# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
crawl weibo content

@author guoweikuang
"""
# import grequests
from common.session_client import session_client
from common.utils import verify_response_status
from common.redis_client import Cache


class Spider(object):
    """crawl module"""
    def __init__(self, base_url, name):
        self.base_url = base_url
        self.name = name
        self.session = session_client(name=name)

    @verify_response_status(200)
    def get_response(self, page=1):
        url = self.base_url + "?page={}".format(page)
        response = self.session.get(url)
        print(response.text)
        return response
