# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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