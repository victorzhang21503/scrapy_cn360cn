'''
###########################################################################################################
# Ihis code is used to crawl all the company data in www.cn360cn.com except the company updated after 2016 
###########################################################################################################
'''

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
	# There are about 43 business category, The milestone and interval is used to crawl the category in range(milestone, milestone + interval), which helpers
	# split the job to smaller ones.
    mileStone = 9
    interval = 8
    name = "cn360cn3-9"
    allowed_domains = ["cn360cn.com"]
    start_urls = []
	
	# There are totally 31 provinces. By modifing the range, we could split the job into the smaller ones which are more controllable 
    for i in range(3, 4):
        start_urls.append('http://www.cn360cn.com/province_' + str(i) + '.aspx')


    def parse(self, response):
        req = []
        hxs = Selector(response)
        urls = hxs.xpath('//div[@id = "divhangye"]/a/@href').extract()
        i = 0
        for url in urls:
            i += 1
            urlChip = url.split('/')
            if len(urlChip) >= 3:
                suffix = "/" + urlChip[-3] + "/" + urlChip[-2] + "/"
                if i in range(self.mileStone, self.mileStone + self.interval):
                    url = "http://www.cn360cn.com" + suffix
                    r = Request(url, callback = self.parseCategory)
                    req.append(r)
                else:
                    pass
        return req

    def parseCategory(self, response):
        req = []
        hxs = Selector(response)
        prefix = response.url
        r = Request(response.url, callback = self.parsePage)
        index = hxs.xpath('//div[@class = "ppage"]//@href').extract()
        if index != []:
            lastPage = index[-1]
            i = 1
            while True:
                i += 1
                suffix = "index_" + str(i) + ".htm"
                url = prefix + suffix
                r = Request(url, callback = self.parsePage)
                req.append(r)
                if suffix == lastPage:
                    break
        return req

    def parsePage(self, response):
        req = []
        url = response.url
        reg = r'(.+?)index'
        mylist = re.findall(reg,url)
        hxs = Selector(response)
        if mylist != []:
            prefix = mylist[0]
            suffix = hxs.xpath('//div[@id = "divcompany1"]//li/a/@href').extract()
            for suf in suffix:
                url = prefix + suf
                r = Request(url, callback = self.parseCn360cn)
                req.append(r)
            return req


    def parseCn360cn(self, response):
        hxs = Selector(response)
        url = response.url
        company = hxs.xpath('//div[@id = "companyname"]/text()').extract()
        if company != []:
            inc = company[0].strip().strip('"').replace('\n',' ').replace('\r',' ').replace('"','\'').replace("\\","/")
            if inc[0] > u'\uf000':
                try:
                    with open("failUrl.txt", "a") as f:
                        f.write(url + "#")
                except IOError as err:
                    print str(err)
            else:
                item = Cn360cnItem()
                space = ' '
                item['url'] = url.strip().strip('"')
                item['company'] = inc 
                descriptions = hxs.xpath('//*[@id="divcenter"]/div[9]/text()').extract()
                if descriptions != []:
                    description = ""
                    for des in descriptions:
                        description += des.strip().strip('"').replace(' ','').replace(' ','').replace(' ','')
                    item['description'] = space.join(description.split()).replace('\n',' ').replace('\r',' ').replace('"','\'').replace("\\","/")
                person = hxs.xpath('//*[@id="divcenter"]/div[15]/div[1]/table/tr[1]/td[2]/text()').extract()
                if person != []:
                    contact_person = person[0].strip().strip('"')
                    contact_person = space.join(contact_person.split()).replace('\n',' ').replace('\r',' ')
                    item['contact_person'] = contact_person
                    list = contact_person.split(' ', 2)
                    if len(list) >= 1:
                        item['name'] = list[0]
                    if len(list) >= 2:
                        if list[1] == u'先生':
                            item['sex'] = u'男'
                        elif list[1] == u'女士':
                            item['sex'] = u'女'

                    if len(list) >=3:
                        item['position'] = list[2][1:(len(list[2])-1)]

                phone = hxs.xpath('//*[@id="divcenter"]/div[15]/div[1]/table/tr[2]/td[2]/text()').extract()
                if phone != []:
                    item['phone'] = phone[0].strip().strip('"').split(',')

                fax = hxs.xpath('//*[@id="divcenter"]/div[15]/div[1]/table/tr[3]/td[2]/text()').extract()
                if fax != []:
                    item['fax'] = fax[0].strip().strip('"')

                address = hxs.xpath('//*[@id="divcenter"]/div[15]/div[1]/table/tr[4]/td[2]/text()').extract()
                if address != []:
                    item['address'] = space.join(address[0].strip().strip('"').split()).replace('\n',' ').replace('\r',' ').replace('"','\'').replace("\\","/")


                zip = hxs.xpath('//*[@id="divcenter"]/div[15]/div[1]/table/tr[5]/td[2]/text()').extract()
                if zip != []:
                    item['zip_code'] = zip[0].strip().strip('"')


                website = hxs.xpath('//*[@id="divcenter"]/div[15]/div[1]/table/tr[6]/td[2]/a/@href').extract()
                if website != []:
                    item['website'] = website[0].strip().strip('"')

                yield item








