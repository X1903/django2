# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class QuotetutorialPipeline(object):

    def open_spider(self, spider):
        '''链接MongoDB'''
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.collection = self.client["toscrape"][spider.name]

    def process_item(self, item, spider):
        '''插入数据到MongoDB'''
        self.collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        '''关闭MongoDB'''
        self.client.close()
