# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient

# 数据去重
import hashlib
import redis


class BookPipeline(object):
    def open_spider(self, spider):
        # 链接MongoDB
        self.client = MongoClient(host='127.0.0.1', port=27017)
        self.collection = self.client["book"][spider.name]

        # 链接Redis
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=2)
        self.item_key = "item_dumpkey"

    def process_item(self, item, spider):
        print("*" * 100)
        # 保存数据到MongoDB,,创建数据表名为爬虫的名
        item_exist = self.item_dupfilter(item)
        if not item_exist:
            self.collection.insert(dict(item))
        return item

    def item_dupfilter(self, item):
        # 数据去重,已有的数据不再存储
        f = hashlib.sha1()
        f.update(item["book_name"].encode())
        f.update(item["book_sku"].encode())
        fingerprint = f.hexdigest()
        added = self.r.sadd(self.item_key, fingerprint)
        return added == 0

    def close_spider(self, spider):
        self.client.close()
