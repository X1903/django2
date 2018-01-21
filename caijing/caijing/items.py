# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CaijingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhongcaiItem(scrapy.Item):
    news_class= scrapy.Field()         # 新闻分类
    news_class_url = scrapy.Field()    # 新闻列表

    news_title = scrapy.Field()        # 新闻标题
    news_url = scrapy.Field()          # 新闻的url
    news_create_time = scrapy.Field()  # 新闻创建时间
    news_text = scrapy.Field()         # 新闻内容



class XinlangItem(scrapy.Item):
    news_url = scrapy.Field()
    news_title = scrapy.Field()
    stitle = scrapy.Field()
    intro = scrapy.Field()
    ctime = scrapy.Field()
    mtime = scrapy.Field()
    intime = scrapy.Field()
    keywords = scrapy.Field()
    media_name = scrapy.Field()
    text = scrapy.Field()
