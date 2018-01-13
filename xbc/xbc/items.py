# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class XbcItem(scrapy.Item):
    # define the fields for your item here like:
    class_name = scrapy.Field()     # 课程名称
    # class_url = scrapy.Field()      #　课程内连接
    # next_url =scrapy.Field()        #　详细页　下一页的url
    # content =scrapy.Field()         # 详细页　中选项
    # title = scrapy.Field()          # 详细页　中题目
    #
    # de_tatie = scrapy.Field()
    # de_url  = scrapy.Field()
    #
    #
    # problem = scrapy.Field()        # 问题题目
    # abcd = scrapy.Field()           # 选择题选项
    # results = scrapy.Field()        # 选择题答案
    # tk_next = scrapy.Field()        # 下一页

    subjects = scrapy.Field()   # 课程名称
    chapter = scrapy.Field()    # 章节标题
    problem = scrapy.Field()    # 题目
    problem_url = scrapy.Field()# 题目的url用于去重
    options = scrapy.Field()    # 问题选项
    result = scrapy.Field()     # 答案


