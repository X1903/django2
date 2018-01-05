# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import JdBookItem
from copy import deepcopy
import json


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        jpy = PyQuery(response.text)

        dt_list = jpy("#booksort > div.mc > dl > dt").items()
        for dt in dt_list:
            item = JdBookItem()

            # 获取大分类的名称
            item["b_cate"] = dt('a').text()

            em_list = dt.next()('em').items()
            for em in em_list:
                # 获取小分类的名称
                item["s_cate"] = em('a').text()
                item["s_href"] = "http:" + em('a').attr("href")
                if item["s_href"] is not None:
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    # 获取列表页的数据
    def parse_book_list(self, response):
        item = response.meta["item"]
        jpy = PyQuery(response.text)
        li_list = jpy('#plist > ul > li').items()
        for li in li_list:
            # 图书名称,作者,出版社,出版时间,图片地址,图书sku编号
            item["book_name"] = li('div > div.p-name > a > em').text()
            item["book_autho"] = li('div > div.p-bookdetails > span.p-bi-name > span.author_type_1 > a').text()
            item["book_press"] = li('div > div.p-bookdetails > span.p-bi-store > a').text()
            item['book_time'] = li('div > div.p-bookdetails > span.p-bi-date').text()

            item["book_img"] = li('div.p-img > a > img').attr('src')
            if item["book_img"]:
                item["book_img"] = "http:" + item["book_img"]
            else:
                item["book_img"] = "http:" + li('div > div.p-img > a > img').attr('data-lazy-img')

            item["book_sku"] = li('div.j-sku-item').attr('data-sku')

            # 判断是否有商品sku,然后获取价格
            if item['book_sku'] is not None:
                # 商品价格json的URL格式
                price_url_tmep = 'http://p.3.cn/prices/get?&pduid=1511765305595946371177&skuid=J_{}'.format(
                    str(item['book_sku']))

                yield scrapy.Request(
                    price_url_tmep.format(item["book_sku"]),
                    callback=self.parse_book_price,
                    meta={"item": deepcopy(item)}
                )
        # 翻页处理
        next_url = jpy('#J_bottomPage > span.p-num > a.pn-next').attr('href')
        if next_url is not None:
            next_url = "http://list.jd.com/" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={'item': item}
            )

    def parse_book_price(self, response):
        # 京东商品价格数据格式
        # [
        #     {
        #         op: "41.20",
        #         m: "55.00",
        #         id: "J_11694204",
        #         p: "41.20"
        #     }
        # ]

        item = response.meta["item"]
        dict_response = json.loads(response.body.decode())
        item["book_price"] = dict_response[0]['op']

        return item


'''

http://p.3.cn/prices/get?&pduid=1511765305595946371177&skuid=J_11956999

http://p.3.cn/prices/get?type=1&area=1_72_4137&ext=11000000&pin=&pdtk=&pduid=1511765305595946371177&pdpin=&pdbp=0&skuid=J_11956999&callback=cnp
http://p.3.cn/prices/get?type=1&area=1_72_4137&ext=11000000&pin=&pdtk=&pduid=1511765305595946371177&pdpin=&pdbp=0&skuid=J_11694204&callback=cnp
http://p.3.cn/prices/get?type=1&area=1_72_4137&ext=11000000&pin=&pdtk=&pduid=1511765305595946371177&pdpin=&pdbp=0&skuid=J_12067413&callback=cnp


b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_href = scrapy.Field()
    book_name = scrapy.Field()
    book_img = scrapy.Field()
    book_autho = scrapy.Field()
    book_sku = scrapy.Field()
    book_price = scrapy.Field()

'''
