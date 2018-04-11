# -*- coding: utf-8 -*-
from login.login import Login
from crawl.weibo import Spider
from crawl.weibo import Parser
from crawl.crawl import async_crawl_weibo


if __name__ == '__main__':
    #login_url = "https://passport.weibo.cn/sso/login"
    #username = ""
    #password = ""
    #login = Login(login_url, username, password)
    #login.login()
    # spider = Spider("https://weibo.cn/gzyhl", name="17317540230")
    # response = spider.get_response(1)
    # print(response)
    # app = Parser(response.text)
    # app.extract_text()

    responses = async_crawl_weibo(start_page=101, end_page=130)
    apps = [Parser(response.text) for response in responses]
    for app in apps:
        app.extract_text()
    apps[0].close_client()
    print(responses)
