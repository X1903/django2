# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from ..items import ZhongcaiItem
from copy import deepcopy


class ZhongcaiSpider(scrapy.Spider):
    name = 'zhongcai'
    allowed_domains = ['cfi.cn']
    start_urls = ['http://industry.cfi.cn/']

    # 根URL
    root_url = 'http://industry.cfi.cn/'

    def parse(self, response):
        doc = pq(response.text)
        li_list = doc('div.breadcrumb > ul > li:gt(0)').items()
        # 遍历分类列表
        for li in li_list:
            item = ZhongcaiItem()
            item['news_class'] = li('a').text()
            item['news_class_url'] = self.root_url + li('a').attr('href')

            yield scrapy.Request(
                item['news_class_url'],
                callback=self.parse_list,
                meta={'item':deepcopy(item)}
            )

    # 提取列表页的信息
    def parse_list(self, response):
        item = response.meta['item']
        doc = pq(response.text)
        a_list = doc('div.zidiv2 > a').items()
        for a in a_list:
            item['news_title'] = a.text()
            item['news_url'] = self.root_url + a.attr('href')

            yield scrapy.Request(
                item['news_url'],
                callback=self.parse_content,
                meta={'item': deepcopy(item)}
            )

        # 翻页处理
        next_url = doc('div.zidiv2 > p > a:last').attr('href')
        if next_url:
            next_url = self.root_url + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_list,
                meta={'item':item}
            )


    # 提取日期和内容
    def parse_content(self, response):
        item = response.meta['item']
        doc = pq(response.text)
        item['news_create_time'] = doc('#tdcontent > table').text()[3:23]  # 时间：2017年09月20日 10:21:43 中财网  截取中间的时间
        item['news_text'] = doc('#tdcontent').remove('h1').remove('table').text()
        yield item
        # print(item)




'''
    news_class= scrapy.Field()         # 新闻分类
    news_class_s_url = scrapy.Field()  # 新闻列表

    news_title = scrapy.Field()        # 新闻标题
    news_url = scrapy.Field()          # 新闻的url
    news_create_time = scrapy.Field()  # 新闻创建时间
    news_text = scrapy.Field()         # 新闻内容
'''