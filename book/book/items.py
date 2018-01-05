# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdBookItem(scrapy.Item):
    b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_href = scrapy.Field()
    book_name = scrapy.Field()
    book_img = scrapy.Field()
    book_autho = scrapy.Field()
    book_sku = scrapy.Field()
    book_price = scrapy.Field()
    book_press = scrapy.Field()
    book_time = scrapy.Field()

class DangdangBookItem(scrapy.Item):
    b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_href = scrapy.Field()
    book_name = scrapy.Field()
    book_img = scrapy.Field()
    book_autho = scrapy.Field()
    book_sku = scrapy.Field()
    book_price = scrapy.Field()
    book_press = scrapy.Field()
    book_time = scrapy.Field()


class AmazonBookItem(scrapy.Item):
    b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_href = scrapy.Field()
    book_name = scrapy.Field()
    book_img = scrapy.Field()
    book_autho = scrapy.Field()
    book_sku = scrapy.Field()
    book_price = scrapy.Field()
    book_press = scrapy.Field()
    book_time = scrapy.Field()