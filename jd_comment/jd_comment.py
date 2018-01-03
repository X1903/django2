# _*_ coding:utf-8 _*_
__author__ = 'Xbc'

import requests
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}


f = open("./jd_comment.txt", 'a', encoding="utf-8")

for i in range(0, 200):
    try:
        print("正在爬去第"+str(i)+"页")
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv16303&productId=1593516&score=0&sortType=5&page='+str(i)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
        response = requests.get(url, headers=headers).text

        res = re.findall('"content":"(.*?)","', response)
        for i in res[::2]:
            i = i.replace("\\n", "")
            f.write(i)
            f.write("\n")
    except:
        print('抓取第'+str(i)+'失败')
f.close()


