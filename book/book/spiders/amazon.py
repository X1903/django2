# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import AmazonBookItem
from copy import deepcopy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/book/all_category/ref=sv_b_1']

    def parse(self, response):
        jpy = PyQuery(response.text)

        # 获取列表页的大分类小分类和小分类的列表页URL
        div_list = jpy('#content > div.a-row.a-size-base:lt(1)').items()
        for div in div_list:
            item = AmazonBookItem()
            item['b_cate'] = div('span.a-color-state').text()

            tbody_list = div('a.a-link-nav-icon').items()
            for tbody in tbody_list:
                item['s_cate'] = tbody.text()
                item['s_href'] = tbody.attr('href')

                if item['s_href'] is not None:
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta={'item': deepcopy(item)}
                    )

    # 获取书籍的信息
    def parse_book_list(self, response):
        item = response.meta['item']
        jpy = PyQuery(response.text)

        li_list = jpy('li.s-result-item.celwidget').items()
        for li in li_list:
            item['book_name'] = li('h2').text()
            item['book_img'] = li('.s-access-image.cfMarker').attr('src')
            item['book_autho'] = li('div.a-row.a-spacing-small > div:eq(1) > span:gt(0)').text()
            item['book_sku'] = li.attr('data-asin')
            item['book_price'] = li('.s-price:eq(0)').text()
            item['book_time'] = li('div.a-row.a-spacing-small > div:eq(0) > span.a-size-small.a-color-secondary').text()
            yield item 
         
        # 翻页处理   
        next_url = jpy('#pagnNextLink').attr('href')
        if next_url is not None:
            next_url = 'https://www.amazon.cn' + next_url
            print(next_url)
            print("+"*150)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={'item':item}
            )


'''
li.s-result-item.celwidget


https://www.amazon.cn/dp/B01ER44LMC/ref=lp_658499051_1_1?s=books&ie=UTF8&qid=1515137771&sr=1-1
https://www.amazon.cn/dp/B071RFQMCG/ref=lp_658499051_1_3?s=books&ie=UTF8&qid=1515137771&sr=1-3
https://www.amazon.cn/dp/B0011BQ23G/ref=lp_658499051_1_1?s=books&ie=UTF8&qid=1515137737&sr=1-12
https://www.amazon.cn/dp/B06XYSX2PC/ref=lp_658393051_1_1?s=books&ie=UTF8&qid=1515136141&sr=1-1
https://www.amazon.cn/dp/B00JZ96ZI8/ref=lp_658393051_1_2?s=books&ie=UTF8&qid=1515136141&sr=1-2


div.a-column > table > tbody
#content > div

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
