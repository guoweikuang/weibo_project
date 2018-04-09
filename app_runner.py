# -*- coding: utf-8 -*-
from login.login import Login
from crawl.weibo import Spider


if __name__ == '__main__':
    #login_url = "https://passport.weibo.cn/sso/login"
    #username = ""
    #password = ""
    #login = Login(login_url, username, password)
    #login.login()
    spider = Spider("https://weibo.cn/gzyhl", name="17317540230")
    response = spider.get_page(2)
    print(response)