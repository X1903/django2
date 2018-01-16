# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):
    '''截取字符串'''

    def __init__(self):
        '''初始字符串长度'''
        self.limit = 50

    def process_item(self, item, spider):
        '''字符串长度超过50截取,然后加上...'''
        if item['content']:
            if len(item['content']) > self.limit:
                item['content'] = item['content'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        '''初始化MongoDB数据库'''
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''scrapy内置函数,可以调用settis里面的变量'''
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        '''爬虫启动的时候调用'''
        # MongoDB初始化链接
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        '''处理数据'''
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        '''关闭spider的时候关闭MongoDB数据库'''
        self.client.close()
