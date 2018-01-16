# _*_ coding:utf-8 _*_
__author__ = 'Xbc'

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-16 00:13:19
# Project: tripadvisor

from pyspider.libs.base_handler import *
import pymongo


class Handler(BaseHandler):
    crawl_config = {
    }
    client = pymongo.MongoClient('127.0.0.1')
    db = client['tripadvisor']

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Attractions-g294217-Activities-Hong_Kong.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.attraction_element div.photo_booking.non_generic > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        next = response.doc('.pagination .next').attr.href
        self.crawl(next, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "name": response.doc('.heading_title').text(),
            "rating": response.doc('.header_rating .more span').text(),
            "address": response.doc('.blRow .address span:gt(0)').text(),
            "phone": response.doc('.phone.directContactInfo span:eq(1)').text(),
            "duration": response.doc('.detail_section.duration').remove('span').text()
        }

    def on_result(self, result):
        if result:
            self.save_to_mongo(result)

    def save_to_mongo(self, result):
        if self.db['Hong_Kong'].insert(result):
            print('save to mongo', result)