# _*_ coding:utf-8 _*_
__author__ = 'Xbc'

import pymongo
import time
# 链接数据库
client = pymongo.MongoClient('127.0.0.1', 27017)
# 绑定数据库名和表明
Mongo = client['taobao']['search']

while True:
    time.sleep(1)
    # 查询MongoDB
    print(Mongo.count())