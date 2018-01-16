# _*_ coding:utf-8 _*_
__author__ = 'Xbc'

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-16 15:02:16
# Project: TmallStore

from pyspider.libs.base_handler import *
import pymongo


class Handler(BaseHandler):
    crawl_config = {
    }

    client = pymongo.MongoClient('127.0.0.1')
    db = client['TmallStore']

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(
            'https://handuyishe.tmall.com/category.htm?spm=a1z10.3-b-s.w4011-14593428692.326.7ab3b8baBXe9kg&scene=taobao_shop&pageNo=1#anchor',
            callback=self.index_page, fetch_type='js')

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.item-name.J_TGoldData').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

        next = response.doc('#J_ShopSearchResult > div > div.J_TItems > div.pagination > a.J_SearchAsync.next').attr(
            'href')
        if next:
            self.crawl(next, callback=self.index_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):

        # 获取物品描述分数
        shopid = response.doc('#LineZing').attr('shopid')
        # desc_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s'.format(shopid)
        # desc = self.crawl(desc_url, callback=self.desc_json)



        return {
            "url": response.url,
            "shopID": shopid,
            "标题": response.doc('.tb-detail-hd h1').text(),
            "价格": response.doc('.tm-price:eq(1)').text(),
            "销量": response.doc('li.tm-ind-item.tm-ind-sellCount > div > span.tm-count').text(),
            "评论": response.doc('#J_ItemRates > div > span.tm-count').text(),
            "图片": response.doc('#J_ImgBooth').attr('src').replace('_430x430q90.jpg', ''),
            # "描述": desc
        }

    def desc_json(self, response):
        return response.json.jsonp209(['dsr']['gradeAvg'])

    def on_result(self, result):
        if result:
            self.save_to_mongo(result)

    def save_to_mongo(self, result):
        if self.db['韩都衣舍'].insert(result):
            print('save to mongo', result)

    class Handler(BaseHandler):
        crawl_config = {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        }



