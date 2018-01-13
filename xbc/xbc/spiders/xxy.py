# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
import re

from ..items import XbcItem
from copy import deepcopy
from pyquery import PyQuery as pq


class XxySpider(scrapy.Spider):
    name = 'xxy'
    allowed_domains = ['sxmaps.com']
    start_urls = ['http://wap.i.sxmaps.com/index.php/public/login.html']
    root_url = 'http://wap.i.sxmaps.com'

    # 登录
    def start_requests(self):
        driver = webdriver.Chrome()
        driver.get('http://wap.i.sxmaps.com/index.php/public/login.html')
        driver.find_element_by_id("account").send_keys("15999999999")
        driver.find_element_by_id("psw").send_keys("888888")
        driver.find_element_by_id("login-btn").click()

        time.sleep(3)
        cookie = driver.get_cookies()

        response = driver.page_source

        next_url = re.findall(r'<a href="(.*?)">我的题库</a>', response)
        url = self.root_url + next_url[0]
        self.cookie_data = {}
        self.cookie_data["PHPSESSID"] = cookie[0]["value"]

        yield scrapy.Request(
            url,
            cookies=self.cookie_data,
            callback=self.parse
        )

    # 获取课程的名称和各个课程题库的URL
    def parse(self, response):
        doc = pq(response.text)
        li_list = doc('div.subject_con > div > ul > li').items()
        
        for li in li_list:
            Item = XbcItem()

            # 题库科目名称
            Item['subjects'] = li('.tit-1 p').text()
            subjects_url = self.root_url + li('a').attr('href')

            yield scrapy.Request(
                subjects_url,
                cookies=self.cookie_data,
                callback=self.detail_list,
                meta={"Item":deepcopy(Item)}
            )


    # 获取课程章节列表页信息
    def detail_list(self, response):
        Item = response.meta["Item"]
        doc = pq(response.text)
        li_list = doc("div.subject_box.chapter_box > div > div > ul > li").items()
        for li in li_list:
            Item['chapter'] = li('.tit p').text()
            chapter_url = li('a').attr('onclick')
            chapter_url = self.root_url + re.findall(r"window.location.href='(.*?)'", chapter_url)[0]
            yield scrapy.Request(
                chapter_url,
                dont_filter=True,
                cookies=self.cookie_data,
                callback=self.content_url,
                meta={"Item": deepcopy(Item)}
            )
            
    # 获取每科每章节的所有题库的URL
    def content_url(self, response):
        Item = response.meta['Item']
        doc = pq(response.text)

        # url 列表
        li_list = doc('div.card_answer_main ul li').items()
        for li in li_list:
            Item['problem_url'] = self.root_url + li('a').attr('href')
            yield scrapy.Request(
                Item['problem_url'],
                cookies=self.cookie_data,
                callback=self.detail_content,
                meta={'Item':deepcopy(Item)}
            )
            
        
    # 获取题库内容
    def detail_content(self, response):
        Item = response.meta["Item"]
        try:
            doc = pq(response.text)
        except Exception:
            pass

        # 获取题库问题
        Item['problem'] = doc('a.preWord').text()
        # 获取选择题选项
        Item['options'] = doc('div.radioboxDiv label').text()
        if Item['options'] == '':
            Item['options'] = doc('.checkboxDiv label').text()
        
        # 获取答案
        Item['result'] = doc('div.dwellBox > pre').text()
        yield Item

        # yield Item


'''


subjects = scrapy.Field()   # 课程名称
chapter = scrapy.Field()    # 章节标题
problem = scrapy.Field()     # 题目
options = scrapy.Field()    # 问题选项
result = scrapy.Field()     # 答案



http://wap.i.sxmaps.com/index.php/Lessontiku/questionsmore_manage/subjectid/86/sectionid/7225/p/22/majorid_sx/38/classid_sx/24
http://wap.i.sxmaps.com/index.php/Lessontiku/questionsmore_manage/subjectid/86/sectionid/7225/p/25/majorid_sx/38/classid_sx/24
http://wap.i.sxmaps.com/index.php/Lessontiku/questionsmore_manage/subjectid/111/sectionid/5014/p/13/majorid_sx/38/classid_sx/24
http://wap.i.sxmaps.com/index.php/Lessontiku/questionsmore_manage/subjectid/203/sectionid/7661/p/2/majorid_sx/38/classid_sx/24


'''
