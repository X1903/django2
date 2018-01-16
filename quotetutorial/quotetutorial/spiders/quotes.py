# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from ..items import QuotetutorialItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        doc = pq(response.text)
        div_list = doc('.col-md-8 .quote').items()
        for div in div_list:
            item = QuotetutorialItem()
            item['content'] = div('.text').text()
            item['author'] = div('.author').text()
            item['tags'] = div('a.tag').text()
            yield item
        next_url = doc('.pager .next a').attr('href')
        if next_url:
            next_url = 'http://quotes.toscrape.com/' + next_url
            print("+."*100)
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
