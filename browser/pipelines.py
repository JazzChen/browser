# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from browser.db import BrowserTable


class CheckPipeline(object):
    def process_item(self, item, spider):
        pass


class EncodingPipeline(object):
    def process_item(self, item, spider):
        for key in item:
            item[key] = item[key].encode('utf-8')
        return item


class MySQLPipeline(object):
    def __init__(self, host, username, password, db):
        self.host = host
        self.username = username
        self.password = password
        self.db = db

    def process_item(self, item, spider):
        try:
            self.table.insert(item['account'], item['deviceid'], item['url'], item['title'],
                              item['idate'], item['logtime'], item['importday'], item['html'], item['text'])
        except Exception as e:
            pass

        return item

    @classmethod
    def from_settings(cls, settings):
        host = settings['MYSQL_HOST']
        username = settings['MYSQL_USERNAME']
        password = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        return cls(host, username, password, db)

    def open_spider(self, spider):
        import MySQLdb
        # create_table is default true

        self.conn = MySQLdb.connect(self.host, self.username,
                                    self.password, self.db, charset='utf8')
        self.table = BrowserTable(self.conn, spider.name, cache_size=100)

    def close_spider(self, spider):
        self.table.flush()
        self.conn.close()

