# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~
sensitive

@author guoweikuang
"""
from collections import defaultdict
from common.const import sensetive
from common.const import sensetive_dict
from common.mysql_client import get_mysql_client
from common.utils import filter_url_mark
from common.logger import logger


class Sensitive(object):
    def __init__(self, rows):
        self.rows = rows
        self.contents = defaultdict(list)
        self.client = get_mysql_client()
        self.urls = []

    def find_sensitive_from_mysql(self):
        for row in self.rows:
            for word in sensetive:
                if word in row[0] and self.filter_text(row[0]):
                    for sen, words in sensetive_dict.items():
                        if word in words:
                            print(sen, word)
                            self.save_sensitive_to_mysql(row[0], sen, word, row)

    # def is_repeat(self, url):
    #     for row in self.rows:
    #         mark = filter_url_mark(row[6]).encode('utf-8')
    #         self.urls.append(mark)
    #     filter_url = filter_url_mark(url).encode('utf-8')
    #     if filter_url in self.urls:
    #         return False
    #     return True
    def filter_text(self, text):
        if '跳楼大甩卖' in text or '跳楼价' in text:
            return False
        return True

    def is_repeat_text(self, text):
        texts = self.read_sensitive_from_mysql()
        texts = [text[0] for text in texts]
        print(texts)
        print(text in texts)
        #assert text in texts
        if text in texts:
            return False
        return True

    def save_sensitive_to_mysql(self, title, event, sensitive, row):
        print(title, event, sensitive, row[3])
        pub_time = row[3].strip()
        try:
            sql = "INSERT INTO opinion(event_type, sen_word, weibo_text, pub_time, comment, like_num) " \
                  "VALUES(%s, %s,%s, %s, %s, %s);"
            #sql = sql % (event, sensitive, title, pub_time)
            #print(self.is_repeat_text(title))
            if not self.is_repeat_text(title):
                return

            self.client.cur.execute(sql, (event, sensitive, title, pub_time, str(row[1]), str(row[2])))
            self.client.conn.commit()
        except Exception as e:
            logger.info("mysql error: %s" % e)
            self.client.conn.rollback()

    def read_sensitive_from_mysql(self):
        sql = "SELECT weibo_text FROM opinion;"
        self.client.cur.execute(sql)
        contents = self.client.cur.fetchall()
        return contents


def run_sensitive(rows):
    sensitive = Sensitive(rows=rows)
    sensitive.find_sensitive_from_mysql()





