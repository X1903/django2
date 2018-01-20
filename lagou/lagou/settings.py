# -*- coding: utf-8 -*-

# Scrapy settings for lagou project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lagou'

SPIDER_MODULES = ['lagou.spiders']
NEWSPIDER_MODULE = 'lagou.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding':'gzip, deflate, br',
#     'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
#     'Cache-Control':'max-age=0',
#     'Connection':'keep-alive',
#     'Cookie':'index_location_city=%E6%B7%B1%E5%9C%B3; _ga=GA1.2.1122321108.1515326984; user_trace_token=20180107200943-a553fe89-f3a3-11e7-a01c-5254005c3644; LGUID=20180107200943-a55402bd-f3a3-11e7-a01c-5254005c3644; JSESSIONID=ABAAABAABEEAAJA6DFE1BCFCC857B04C8AB957B19A67B0F; _gid=GA1.2.447432044.1516251586; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515663330,1515769944,1516251586,1516251680; TG-TRACK-CODE=index_navigation; LGSID=20180118150512-ed7b4a50-fc1d-11e7-a83d-525400f775ce; X_HTTP_TOKEN=b38f0681cb31971c4e5be13a45192ce4; _putrc=A9A5E87BA959D23A; login=true; unick=%E5%BE%90%E5%BF%83%E6%84%BF; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=6849981b817d660be016d8b38a84ed55c77180ce7f1ccacc; SEARCH_ID=e62c00313f2c42cb8328216d55227281; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516263180; LGRID=20180118161306-69671e36-fc27-11e7-a4c3-5254005c3644',
#     'Host':'www.lagou.com',
#     'Referer':'https://www.lagou.com/zhaopin/Java/?labelWords=label',
#     'Upgrade-Insecure-Requests':'1',
#     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lagou.middlewares.LagouSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html


DOWNLOADER_MIDDLEWARES = {
   # 'lagou.middlewares.LagouDownloaderMiddleware': 543,
   # 'lagou.middlewares.ProxyMiddleware': 100,
   'lagou.middlewares.RandomProxyMiddleware': 99,
   # 'lagou.middlewares.RandomUserAgentMiddlware': 100,

}




# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'lagou.pipelines.LagouPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
