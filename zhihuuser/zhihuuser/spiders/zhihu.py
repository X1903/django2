# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import UserItem
import json


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]


    # 初始用户
    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'

    # 粉丝列表
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # 获取第一用的信息,交给parse_user处理,获取返回的item
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)

        # 关注列表信息交给parse_follows处理, 获取用户的信息
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),
                      callback=self.parse_follows)

        # 获取粉丝列表的信息,交给parse_follows处理,获取粉丝的信息
        yield  Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
                       callback=self.parse_followers)

    # 发起第一请求,即入口
    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)

        yield item

        # 对每一个关注的用户进行递归处理
        yield Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0), callback=self.parse_follows)
        yield Request(self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0), callback=self.parse_followers)

    def parse_follows(self, response):
        results = json.loads(response.text)

        # 对用户关注的人进行解析
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        # 对下一页进行处理
        if "paging" in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, callback=self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)

        # 对用户关注的人进行解析
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        # 对下一页进行处理
        if "paging" in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, callback=self.parse_followers)