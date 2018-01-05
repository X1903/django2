# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
import time
import re
import requests


       # /index.php/lessontiku/tiku_manage.html
class ShengxueSpider(scrapy.Spider):
    name = 'shengxue'
    allowed_domains = ['sxmaps.com']
    start_urls = ['http://i.sxmaps.com/index.php/member/login.html']

    def __init__(self):
        driver = webdriver.Chrome()
        driver.get('http://i.sxmaps.com/index.php/member/login.html')
        driver.find_element_by_id("username").send_keys("15999692363")
        driver.find_element_by_id("password").send_keys("xy0808")
        driver.find_element_by_id("login_button").click()
        cookie = driver.get_cookies()

        time.sleep(3)

        response = driver.page_source

        next_url = re.findall(r'<a href="(.*?)">我的题库<em></em></a>', response)
        # print(url)
        root_url = 'http://i.sxmaps.com'
        url = root_url + next_url[0]
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
        # [{'value': 'n7c8mavvr6gsgs0uacs7dtg794', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'domain': 'i.sxmaps.com', 'secure': False}]
        cookie_data = {}
        cookie_data["PHPSESSID"] = cookie[0]["value"]

        yield scrapy.Request(
            url,
            headers=headers,
            cookies=cookie_data,
            callback=self.parse
        )



    def parse(self, response):
        print(response.body)
        # form_data = {
        #     "phone": "15999692363",
        #     "password": "xy0808",
        #     "rember_me": "0"
        # }
        # yield scrapy.FormRequest(
        #     "http://i.sxmaps.com/index.php/live/zb.html",
        #     formdata = form_data,
        #     callback = self.parse_login
        # )


    def parse_login(self, response):
        print("*" * 100)
        print(re.findall("徐", response.body.decode()))
        print("+" * 100)

    # "http://i.sxmaps.com/index.php/live/zb.html"

    def login_request(self):
        pass