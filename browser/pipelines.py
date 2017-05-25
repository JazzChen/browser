# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.exceptions import DropItem

from crawler.items import BrowserItem
from crawler.db import good_Table

class CheckPipeline(object):
    def process_item(self,item,spider):
        for key in item:
            if item[key]==None:
                raise DropItem('%s is missing %s' % (item,key))
        return item

class EncodingPipeline(object):
    def process_item(self,item,spider):
        for key in item:
            item[key]=item[key].encode('utf-8')
        return item

class MySQLPipeline(object):
    def __init__(self,host,username,password,db):
        self.host = host
        self.username = username
        self.password = password
        self.db = db

    def process_item(self,item,spider):
        try:
            self.table.insert(item['mall'],item['rank'],item['title'],item['price'],
                          item['turnover_index'],item['top_id'],item['type_id1'],item['type_id2'],item['url'])
        except Exception as e:
            pass

        return item

    @classmethod
    def from_settings(cls,settings):
        host=settings['MYSQL_HOST']
        username=settings['MYSQL_USERNAME']
        password=settings['MYSQL_PASSWORD']
        db=settings['MYSQL_DB']
        return cls(host,username,password,db)

    def open_spider(self,spider):
        import MySQLdb
        #create_table is default true

        self.conn=MySQLdb.connect(self.host,self.username,
                                  self.password,self.db,charset='utf8')
        self.table=good_Table(self.conn,spider.name,cache_size=100)

    def close_spider(self,spider):
        self.table.flush()
        self.conn.close()

class BrowserPipeline(object):
    def process_item(self, item, spider):
        return item
