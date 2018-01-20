# -*- coding: utf-8 -*-

from copy import deepcopy
import scrapy
from pyquery import PyQuery as pq
from ..items import LagouItem


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/']

    cookie = {
        'Cookie': 'JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
                  'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644; '
                  'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
                  'index_location_city=%E6%B7%B1%E5%9C%B3; '
                  'TG-TRACK-CODE=index_navigation; _gat=1; '
                  '_gid=GA1.2.807135798.1504227456; _ga=GA1.2.1721572155.1504227456; '
                  'LGSID=20170901085741-8ea70793-8eb0-11e7-902f-5254005c3644; '
                  'LGRID=20170901095027-ed9ebf87-8eb7-11e7-902f-5254005c3644; '
                  'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
                  'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504230623;'
                  'SEARCH_ID=a274b85f40b54d4da62d5e5740427a0a'
    }

    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/60.0.3112.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_java?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
    }
    cookies = {
        'Cookie': 'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644;'
                  'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
                  'index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=7277bc08d137413dac2590cea0465e39; '
                  'TG-TRACK-CODE=search_code; JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
                  'PRE_UTM=; PRE_HOST=; '
                  'PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; '
                  'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3413383.html; _gat=1; _'
                  'gid=GA1.2.807135798.1504227456; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
                  'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504252636; _ga=GA1.2.1721572155.1504227456; '
                  'LGSID=20170901153335-dd437749-8ee7-11e7-903c-5254005c3644; '
                  'LGRID=20170901155728-336ca29d-8eeb-11e7-9043-5254005c3644',
    }

    def parse(self, response):
        doc = pq(response.text)
        dl_list = doc('#sidebar > div > div > div.menu_sub.dn > dl:eq(0)').items()
        for dl in dl_list:
            item = LagouItem()
            item['b_class'] = dl('dt span').text()
            s_class_list = dl('dd a').items()
            for s in s_class_list:
                item['s_class'] = s.text()
                item['s_class_href'] = s.attr('href')
                if item['s_class_href']:
                    yield scrapy.Request(
                        item['s_class_href'],
                        callback=self.parse_job_list,
                        headers=self.headers,
                        cookies=self.cookies,
                        meta={'item': deepcopy(item)}

                    )

    def parse_job_list(self, response):
        item = response.meta['item']
        doc = pq(response.text)
        li_list = doc('#s_position_list ul.item_con_list li').items()
        for li in li_list:
            item['job_title'] = li('div.p_top > a > h3').text()
            item['job_company'] = li('div.company_name > a').text()
            item['job_url'] = li('div.p_top > a').attr('href')
            item['job_price'] = li('.money').text()
            print(item)

            # if item['job_url']:
            #     yield scrapy.Request(
            #         item['job_url'],
            #         callback=self.parse_job_content,
            #         headers=self.header,
            #         meta={'item':deepcopy(item)}
            #     )

            # def parse_job_content(self, response):
            #     item = response.meta['item']
            #     doc = pq(response.text)
            #     item['job_tags'] = doc('li.labels').text()
            #     item['job_suffer'] = doc('.job_request span:nth-child(3)').text()
            #     item['job_xueli'] = doc('.job_request span:nth-child(4)').text()
            #     item['job_youhuo'] = doc('.job-advantage p').text()
            #     item['job_JD'] = doc('#job_detail > dd.job_bt > div > p:nth-child(2)').text()
            #     item['job_addr'] = doc('#job_detail > dd.job-address.clearfix > div.work_addr').text()
            #     item['lingyu'] = doc('#job_company > dd > ul > li:nth-child(1)').remove('a').text()
            #     item['fazhan'] = doc('#job_company > dd > ul > li:nth-child(2)').remove('a').text()
            #     item['guimo'] = doc('#job_company > dd > ul > li:nth-child(3)').remove('a').text()
            #     item['guimo'] = doc('#job_company > dd > ul > li:nth-child(4) a').text()
            #     
            #     
            #     print(item)
            #     print('+'*100)


'''

b_class = scrapy.Field()       # 职位的大分类
s_class = scrapy.Field()       # 小分类
s_class_href = scrapy.Field()  # 小分类的列表页

job_title = scrapy.Field()     # 工作的标题
job_company = scrapy.Field()   # 公司名称
job_url = scrapy.Field()       # 职位的url
job_tags = scrapy.Field()      # 职位的标签
job_price = scrapy.Field()     # 职位的薪资

job_suffer = scrapy.Field()    # 工作经验
job_xueli = scrapy.Field()     # 学历要求
job_youhuo = scrapy.Field()    # 职位诱惑
job_JD = scrapy.Field()        # 职位描述
job_addr= scrapy.Field()       # 工作地址
lingyu = scrapy.Field()        # 公司的领域
fazhan = scrapy.Field()        # 融资情况
guimo = scrapy.Field()         # 公司规模
www = scrapy.Field()           # 公司网址

'''
