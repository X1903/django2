# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from pyquery import PyQuery
from ..items import DangdangBookItem


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com', 'ddimg.cn']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        jpy = PyQuery(response.text)

        dl_list = jpy('div.hide.submenu dl.inner_dl:gt(1)')

        # 获取大分类和小分类及小分类的URL列表
        for dl in dl_list.items():
            item = DangdangBookItem()
            item['b_cate'] = dl('dt').text()
            a_list = dl('dd a').items()
            for a in a_list:
                item['s_cate'] = a.text()
                item['s_href'] = a.attr('href')

                if item['s_href'] is not None:
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta={'item':deepcopy(item)}
                    )
    def parse_book_list(self, response):
        item = response.meta["item"]
        jpy = PyQuery(response.text)

        # 获取图书的信息
        li_list = jpy('ul.bigimg li').items()
        for li in li_list:
            item['book_name'] = li('a.pic').attr('title')
            item['book_img'] = li('a.pic img').attr('data-original')
            item['book_sku'] = li.attr('id').split('p')[-1]
            item['book_price'] = li('p.price span.search_now_price').text()
            item['book_autho'] = li('p.search_book_author > span:eq(0) > a:eq(0)').attr('title')
            item['book_time'] = li('p.search_book_author > span:eq(1)').text()
            item['book_press'] = li('p.search_book_author > span:eq(2) a').attr('title')

            yield item

        # 翻页处理
        next_url = jpy('.paging .next a').attr('href')
        if next_url is not None:
            next_url = 'http://category.dangdang.com/' + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={'item':item}
            )

'''
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
'''

