#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding( "utf-8" )
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from scrapy import log
from cn360cn.items import Cn360cnItem
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.conf import settings

class Cn360cnSpider(Spider):
    dic = {}
    stat = {}
    name = "cn360cnxx"
    allowed_domains = ["cn360cn.com"]
    start_urls = []
    cate = set()
    for i in range(1,32):
        start_urls.append('http://www.cn360cn.com/province_' + str(i) + '.aspx')



    def parse(self, response):
        hxs = Selector(response)
        urls = hxs.xpath('//div[@id = "divhangye"]/a/@href').extract()
        cat  = hxs.xpath('//div[@id = "divhangye"]/a/text()').extract()
        i = 0

        for url in urls:
            urlChip = url.split('/')
            if len(urlChip) >= 3:

                suffix = "/" + urlChip[-3] + "/" + urlChip[-2] + "/"
                url = "http://www.cn360cn.com" + suffix

                if urlChip[-2] not in self.cate:
                    self.cate.add(urlChip[-2])
                    self.dic[urlChip[-2]] = cat[i]
                i += 1

        print self.dic
