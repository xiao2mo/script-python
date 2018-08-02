#-*- coding:utf-8 -*-
import os
import time
import re
import requests
import urlparse
import urllib2
import  json
from bs4 import BeautifulSoup
new_urls=["https://api.douban.com/v2/movie/in_theaters?count=39","https://api.douban.com/v2/movie/coming_soon?count=102"]

#new_urls=["https://m.dianping.com/awp/h5/hotel-dp/shop-detail/index.html?shopId=9947281"]
fout = open('newfilm2.txt', 'w')
if __name__ == "__main__":
    name = set()
    for hotelurl in new_urls:
        #headers = {
            #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}
        headers={
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/49.0.2623.221Safari/537.36SE2.XMetaSr 1.0'
        }
        html_cont = urllib2.Request(url=hotelurl, headers=headers)
        html_cont2=urllib2.urlopen(html_cont).read().decode('utf-8')
        #print html_cont2.encode('utf-8').strip()
        result = json.loads(html_cont2.encode('utf-8').strip())

        for item in result["subjects"]:
            print(item['title'])
            name.add(item["title"])

    for i in name:
        fout.write(i.encode('utf-8').strip())
        fout.write("\n")
    fout.close()























