# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
import re
from xbc import items
from copy import deepcopy


class XxySpider(scrapy.Spider):
    name = 'xxy'
    allowed_domains = ['sxmaps.com']
    start_urls = ['http://wap.i.sxmaps.com/index.php/public/login.html']
    # http://wap.i.sxmaps.com/index.php/public/login.html
    root_url = 'http://wap.i.sxmaps.com'

    def start_requests(self):
        driver = webdriver.Chrome()
        driver.get('http://wap.i.sxmaps.com/index.php/public/login.html')
        driver.find_element_by_id("account").send_keys("15999692363")
        driver.find_element_by_id("psw").send_keys("xy0808")
        driver.find_element_by_id("login-btn").click()

        time.sleep(3)
        cookie = driver.get_cookies()
        # driver.find_element_by_class_name("layui-layer-ico layui-layer-close layui-layer-close2").click()

        response = driver.page_source
        print("------")
        # <a href="/index.php/lessontiku/tiku_manage.html">我的题库</a>
        next_url = re.findall(r'<a href="(.*?)">我的题库</a>', response)
        print(next_url)
        url = self.root_url + next_url[0]
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
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
        # data = response.body
        # print("内容",data)
        class_list = response.xpath("//ul[@class='clearfix']/li")
        for ass in class_list:
            Item = items.XbcItem()
            Item['class_url'] = self.root_url + ass.xpath("./a/@href").extract_first()
            Item['class_name'] = ass.xpath('./p/@text()').extract_first()
            print("-"*100)
            print(Item['class_url'])
            yield scrapy.Request(
                Item['class_url'],
                dont_filter=True,
                meta={"Item": Item},
                callback=self.detail_list
            )

    def detail_list(self, response):
        Item = response.meta.get("Item")
        print("列表页获取的数据", Item)
        de_list = response.xpath("//ul[@class='clearfix']/li")
        for detail in de_list:
            Item["de_tatie"] = detail.xpath(".//p/text()").extract_first()
            # http://wap.i.sxmaps.com
            # window.location.href='/index.php/Lessontiku/questionsmore_manage/sectionid/7219/subjectid/84/p/25/classid_sx/24/majorid_sx/38'
            Item["de_url"] = detail.xpath(".//a[@class='btn']/@onclick").extract_first()
            Item["de_url"] = self.root_url + re.findall(r"window.location.href='(.*?)'", Item["de_url"])[0]
            print("*"*100)
            print(Item['de_url'])
            yield scrapy.Request(
                Item["de_url"],
                meta={"Item": deepcopy(Item)},
                callback=self.detail
            )

    def detail(self, response):
        Item = response.meta.get("Item")
        print("详细列表页获取的内容", Item)
        Item['title'] = response.xpath("//a[@class='preWord']/pre/text()").extract_first()
        Item["content"] = response.xpath("//div[@class='radioboxDiv']//text()").extract()
        # 　/html/body/div/div/div[2]/div[2]/div/div/a[3]
        print("@" * 100)
        print(response.xpath('//a[@class="btn next"]/@onclick'),
              type(response.xpath('//a[@class="btn next"]/@onclick')))
        print("@" * 100)
        Item["next_url"] = response.xpath("//div[@class='jogger']/a[text()='下一题']/@onclick").extract_first()

        qwrurl = "/index.php/Lessontiku/questionsmore_manage"
        # zjpurl = "/index.php/Lessontiku/questions_manage"
        if Item["next_url"] is not None:
            Item["next_url"] = self.root_url + Item["next_url"]
            data = re.findall(r'lesson.questionSubmitNext(\d+);', Item)[0]
            subjectid = response.xpath("//div[@topic_list]/@sub_id").extract_first()
            sectionid = response.xpath("//div[@topic_list]/@seb_id").extract_first()
            qpages = response.xpath("//div[@topic_list/@qpage]").extract_first()
            majorid_sx = response.xpath("//input[@id='classid_sx']/@value").ectract_first()
            classid_sx = response.xpath("//input[@id='majorid_sx']/@value")
            #  <div class="topic_list" qstatus="1" qpage="25" questionid="202106"
            qpages = int(qpages) - 1
            if int(data) == 1:
                Item[
                    "next_url"] = self.root_url + qwrurl + '/subjectid/' + subjectid + '/sectionid/' + sectionid + '/p/' + '%d' % qpages + '/majorid_sx/' + majorid_sx + '/classid_sx/' + classid_sx
                yield scrapy.Request(
                    Item["next_url"],
                    meta={"Item": deepcopy(Item)},
                    callback=self.detail
                )
            elif int(data) == 2:
                Item[
                    "next_url"] = self.root_url + qwrurl + '/subjectid/' + subjectid + '/sectionid/' + sectionid + '/p/' + '%d' % qpages + '/majorid_sx/' + majorid_sx + '/classid_sx/' + classid_sx
                yield scrapy.Request(
                    Item["next_url"],
                    meta={"Item": deepcopy(Item)},
                    callback=self.detail
                )
        else:
            print(Item)
