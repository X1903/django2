# -*- coding: utf-8 -*-
from scrapy import Request
from ..items import ZhilianSpiderItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class ZhilianSpider(RedisCrawlSpider):
    name = 'zhilianspider'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    rules = [
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[3]/div[3]/form/div[1]/div[1]/div[3]/ul/li[11]/a'), follow=True),
        Rule(LinkExtractor(allow=r'http://jobs.zhaopin.com/(\d.+).htm'), callback='parse_zhilian')
    ]

    def start_requests(self):
        url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7%2B%E5%8C%97%E4%BA%AC%2B%E5%B9%BF%E5%B7%9E%2B%E6%B7%B1%E5%9C%B3&kw=%E4%BC%9A%E8%AE%A1'
        yield Request(url, headers=self.headers)

    def parse_zhilian(self, response):
        _ = self
        item = ZhilianSpiderItem()

        item['job_id'] = response.url

        item['job_name'] = response.xpath('/html/body/div[5]/div[1]/div[1]/h1/text()').extract_first()

        item['job_company'] = response.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()').extract_first()

        item['job_salary'] = response.xpath('/html/body/div[6]/div[1]/ul/li[1]/strong/text()').extract_first().strip()

        item['job_education'] = ''.join(response.xpath('/html/body/div[6]/div[1]/ul/li[6]/strong/text()').extract())

        item['job_address'] = ''.join(response.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/h2/text()').extract()).strip()

        item['job_category'] = ''.join(response.xpath('/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()').extract())

        item['job_description'] = ''.join(response.xpath('/html/body/div[6]/div[1]/div[1]/div//p').xpath('string(.)').extract()).replace(',', '，').replace('\r\n', '').strip()
        if not item['job_description']:
            item['job_description'] = ''.join(response.xpath('/html/body/div[6]/div[1]/div[1]/div').xpath('string(.)').extract()).replace(',', '，').replace('\r\n', '').strip()

        text = ''.join(response.xpath(
            '/html/body/div[6]/div[1]/div[1]/div/div[2]//p').xpath('string(.)').extract()).replace(',', '，').replace('\r\n', '').strip()

        if text:
            item['company_profile'] = text

            if item['company_profile'] == '':
                item['company_profile'] = ''.join(response.xpath('/html/body/div[6]/div[1]/div[1]/div/div[2]/text()').extract()).replace(',', '，').replace('\r\n', '').strip()
        else:
            item['company_profile'] = ''.join(response.xpath('/html/body/div[6]/div[1]/div[1]/div/div[2]/div/text()').extract()).replace(',', '，').replace('\r\n', '').strip()

        yield item



