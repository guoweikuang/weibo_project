# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~
crawl weibo content

@author guoweikuang
"""
# import grequests
from common.session_client import session_client
from common.utils import verify_response_status


class Spider(object):
    """crawl module"""
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = session_client()

    @verify_response_status(200)
    def get_page(self, page=1):
        url = self.base_url + "&page={}".format(page)
        response = self.session.get(url)
        return response
