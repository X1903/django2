from urllib.parse import urlencode
import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'IPLOC=CN4403; SUID=DE59E9B72423910A000000005A517370; SUID=DE59E9B73020910A000000005A517370; SUV=003A1752B7ED40465A51737462FEF987; PHPSESSID=c0sj2bqo72amfgqs3abfddaha1; SUIR=1515287525; SNUID=282F82D86E6B0D4A0E7BC7A96F76739A; JSESSIONID=aaa_62pSFxcEofWPTGadw; ABTEST=0|1515287582|v1; ppinf=5|1515287763|1516497363|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTQlQkQlOTUlRTYlQjElODJ8Y3J0OjEwOjE1MTUyODc3NjN8cmVmbmljazoxODolRTQlQkQlOTUlRTYlQjElODJ8dXNlcmlkOjQ0Om85dDJsdUw2YUMyTEg4LS14NkdHYWFSb2pjcTRAd2VpeGluLnNvaHUuY29tfA; pprdig=tRCwKjRQvTi-bk6yjsEeTaVO20wClVC9Z0Vvz8YetXUFQsL9GJ3MFSks-bHz0ljSavhjnLeOb2rI2fupFjhtKWDHbK0KSQ4siDYoewPWQRawrIXQNoZbBqoFnLzOPTJQ096GYsK6bOHu1-mg_sHKIuXq8-enWtJDdZig7CYTem4; ppmdig=15152876920000000b8c767828b117df1161a5e8b4a78f61',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

proxy = None


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):

    global proxy
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('使用代理', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)



def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None

def save_to_mongo(data):
    if db['wx'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for page in range(1, 101):
        print("请求第%s" % page)
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    if article_data:
                        save_to_mongo(article_data)
                    else:
                        print('无数据..............................')



if __name__ == '__main__':
    main()