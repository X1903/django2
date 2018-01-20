# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 随机更换user-agent
from fake_useragent import UserAgent


class RandomUserAgentMiddlware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent(verify_ssl=False)
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        print('使用UA.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.',get_ua())

        request.headers.setdefault('User-Agent', get_ua())


import requests
# 使用ip代理
ip_url = 'http://127.0.0.1:5555/random'
def get_proxy():
    try:
        response = requests.get(ip_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

class RandomProxyMiddleware(object):


    # 动态设置ip代理
    def process_request(self, request, spider):
        request.meta["proxy"] = 'http://' + get_proxy()
        print('使用代理IP............................'+request.meta["proxy"])


import random

class ProxyMiddleware(object):

    def __init__(self):
        self.user_agent_ip_list = [
            '182.37.71.220:6856',
            '121.232.67.124:8736',
            '119.5.181.18:3979',
            '113.27.100.44:5987',
            '114.234.0.123:2736',
            '222.241.116.180:7524',
            '112.85.109.24:1131',
            '139.201.150.93:2356',
            '42.242.166.192:2318',
            '111.76.169.10:5324'
        ]
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxy_ip = random.choice(self.user_agent_ip_list)
        request.meta['proxy'] = proxy_ip
        print('+' * 20, 'the Current ip address is', proxy_ip, '+' * 20)

        # ip from http://pachong.org/

