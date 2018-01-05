# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class XbcItem(scrapy.Item):
    # define the fields for your item here like:
    class_name = scrapy.Field()     # 课程名称
    class_url = scrapy.Field()      #　课程内连接
    next_url =scrapy.Field()        #　详细页　下一页的url
    content =scrapy.Field()         # 详细页　中选项
    title = scrapy.Field()          # 详细页　中题目
    de_tatie = scrapy.Field()
    de_url  = scrapy.Field()