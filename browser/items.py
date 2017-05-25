# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class BrowserItem(scrapy.Item):
    account=Field()
    deviceid=Field()
    url=Field()
    title=Field()
    idate=Field()
    logtime=Field()
    importday=Field()
    html=Field()
    text=Field()
