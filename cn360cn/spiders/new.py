'''
###########################################################################################################
# Ihis code is used to crawl all the company data updated after 2016 in www.cn360cn.com  
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
    name = "cn360cn2016"
    allowed_domains = ["cn360cn.com"]
    start_urls = []
    for i in range(1, 93):
        start_urls.append('http://www.cn360cn.com/company' + str(i) + '.aspx')


    def parse(self, response):
        req = []
        url = response.url
        reg = r'(.+?)company'
        mylist = re.findall(reg, url)
        hxs = Selector(response)
        if mylist != []:
            prefix = mylist[0]
            suffix = hxs.xpath('//div[@id = "divcompany1"]//li/div[1]/a/@href').extract()
            business = hxs.xpath('//div[@id = "divcompany1"]//li/div[1]/text()').extract()
            i = 0
            for suf in suffix:
                url = prefix + suf
                r = Request(url, meta = {'business' : business[i]}, callback = self.parseCn360cn)
                req.append(r)
                i += 1
            return req


    def parseCn360cn(self, response):
        hxs = Selector(response)
        url = response.url
        business = response.meta['business']
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
                item['business'] = business[7:]
                space = ' '
                item['url'] = url.strip().strip('"')
                item['company'] = inc
                descriptions = hxs.xpath('//div[@class = "divcontent"][1]//text()').extract()
                if descriptions != []:
                    description = ""
                    for des in descriptions:
                        description += des.strip().strip('"').replace(' ','').replace(' ','').replace(' ','')
                    item['description'] = space.join(description.split()).replace('\n',' ').replace('\r',' ').replace('"','\'').replace("\\","/")

                person = hxs.xpath('//div[@class = "divcontent"][2]//tr[1]/td/text()').extract()
                if len(person) == 2:
                    contact_person = person[1].strip().strip('"')
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

                phone = hxs.xpath('//div[@class = "divcontent"][2]//tr[2]/td/text()').extract()
                if len(phone) == 2:
                    item['phone'] = phone[1].strip().strip('"').split(',')

                email = hxs.xpath('//div[@class = "divcontent"][2]//tr[3]/td/text()').extract()
                if len(email) == 2:
                    item['email'] = email[1].strip().strip('"').split(',')

                QQ = hxs.xpath('//div[@class = "divcontent"][2]//tr[4]/td/text()').extract()
                if len(QQ) == 2:
                    item['QQ'] = QQ[1].strip().strip('"').split(',')

                address = hxs.xpath('//div[@class = "divcontent"][2]//tr[5]/td/text()').extract()
                if len(address) == 2:
                    item['address'] = space.join(address[1].strip().strip('"').split()).replace('\n',' ').replace('\r',' ').replace('"','\'').replace("\\","/")

                website = hxs.xpath('//div[@class = "divcontent"][2]//tr[6]//a/text()').extract()
                if website != []:
                    item['website'] = website[0].strip().strip('"')

                yield item








