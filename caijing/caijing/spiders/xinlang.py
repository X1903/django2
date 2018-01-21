# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from ..items import XinlangItem
from copy import deepcopy
from pyquery import PyQuery as pq

class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']

    url_json= 'http://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&page={page}'

    def start_requests(self):
        # 8560
        for i in range(180, 8560):
            yield Request(self.url_json.format(page=str(i)), callback=self.parse)

    def parse(self, response):
        result = json.loads(response.body_as_unicode())
        datas = result['result']['data']

        for data in datas:
            item = XinlangItem()

            item['news_url'] = data['url']
            item['news_title'] = data['title']
            item['stitle'] = data['stitle']
            item['intro'] = data['intro']
            item['ctime'] = data['ctime']
            item['mtime'] = data['mtime']
            item['intime'] = data['intime']
            item['keywords'] = data['keywords']

            yield scrapy.Request(
                item['news_url'],
                callback=self.parse_content,
                meta={'item':deepcopy(item)}
            )

    def parse_content(self, response):
        item = response.meta['item']
        doc = pq(response.text)
        item['text'] = doc('#artibody').remove('#ad_44099').text()
        yield item




        # for data in result.keys():
        #     item = XinlangItem()
        #     item['url'] = data['url']
        #     print("+"*100)
        #     print(item)




'''


url = scrapy.Field()
title = scrapy.Field()
s_title = scrapy.Field()
intro = scrapy.Field()
ctime = scrapy.Field()


mtime = scrapy.Field()
intime = scrapy.Field()
keywords = scrapy.Field()
media_name = scrapy.Field()
text = scrapy.Field()
'''

