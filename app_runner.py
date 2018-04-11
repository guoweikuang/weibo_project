# -*- coding: utf-8 -*-
from login.login import Login
from crawl.weibo import Spider
from crawl.weibo import Parser
from crawl.crawl import async_crawl_weibo
from handle_text.tf_idf import TFIDF
from common.mysql_client import get_text_from_mysql
import arrow
from pprint import pprint

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

    #responses = async_crawl_weibo(start_page=1, end_page=3)
    #apps = [Parser(response.text) for response in responses]
    #for app in apps:
    #    app.extract_text()
    #apps[0].close_client()
    #print(responses)
    now = arrow.utcnow().date()
    start = arrow.utcnow().shift(days=-2).date()
    rows = get_text_from_mysql("content", start_time=start, end_time=now)
    tf_idf = TFIDF(rows)
    tf_idf_dict = tf_idf.tf_idf()
    pprint(sorted(tf_idf_dict.items(), key=lambda d:d[1], reverse=True))
    # pprint(rows)