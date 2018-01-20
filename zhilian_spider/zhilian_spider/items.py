# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianSpiderItem(scrapy.Item):
    job_id = scrapy.Field()  # 职位ID
    job_name = scrapy.Field()  # 职位名称
    job_company = scrapy.Field()  # 公司名字
    job_salary = scrapy.Field()  # 职位薪资
    job_education = scrapy.Field()  # 学历需求
    job_address = scrapy.Field()  # 工作地址
    job_category = scrapy.Field()  # 职位类别
    job_description = scrapy.Field()  # 职位描述
    company_profile = scrapy.Field()  # 公司介绍
