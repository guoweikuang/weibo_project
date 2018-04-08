# -*- coding: utf-8 -*-
from login.login import Login


if __name__ == '__main__':
    login_url = "https://passport.weibo.cn/sso/login"
    username = "17317540230"
    password = "gwk2014081029"
    login = Login(login_url, username, password)
    login.login()
