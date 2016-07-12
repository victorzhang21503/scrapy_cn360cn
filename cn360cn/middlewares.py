__author__ = 'huangmeng'
# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random
import json
import re
import threading
from scrapy import log
import time
import urllib
from time import sleep
from scrapy.conf import settings

import os
# Start your middleware class
class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",\
        "Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",\
        "Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)",\
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",\
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",\
        "Googlebot/2.1 (+http://www.googlebot.com/bot.html)",\
        "Googlebot/2.1 (+http://www.google.com/bot.html)",\
        "msnbot/1.0 (+http://search.msn.com/msnbot.htm)"
       ]

class ProxyMiddleware(object):
    def __init__(self, settings):
        self.tmptime=time.time()
        self.pausetime=time.time()
        self.CON = settings.get('CON')
        while True:
            finarr=[]
            try:
                fin = open(self.CON,'r')
                for one in fin:
                    if len(one.strip())>0:
                        finarr.append(one.strip())
                url=''
                if len(finarr[1])>0:
                    url=finarr[1]
                    print url
                    page = urllib.urlopen(url)
                    html = page.read()
                    proxyapi = json.loads(html)
                    data=proxyapi['data']
                    self.proxies = {}
                    for one in data:
                        ip_port=one['proxy'].strip('http://')
                        proxy_address='http://%s' % (ip_port)
                        if ip_port:
                            self.proxies[proxy_address]=ip_port
            except Exception,e:
                sleep(60)
                continue
            if len(self.proxies)>0:
                break
            else:
                sleep(60)
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def process_request(self, request, spider):
        while True:
            finarr=[]
            fin = open(self.CON,'r')
            for one in fin:
                if len(one.strip())>1:
                    finarr.append(one.strip())
            # print finarr[0]
            if finarr[0]=='false':
                break
            else:
                # print 'loop'
                sleep(30)
        days=1*60
        now=time.time()
        t=self.tmptime

        if t+days<now:
            if len(self.proxies)<=10 or  t+days*2<now:
                self.tmptime=now
                while True:
                    print '======================action========================'
                    finarr=[]
                    try:
                        fin = open(self.CON,'r')
                        for one in fin:
                            if len(one.strip())>0:
                                finarr.append(one.strip())
                        url=''
                        if len(finarr[1])>0:
                            url=finarr[1]
                            print url
                            page = urllib.urlopen(url)
                            html = page.read()
                            proxyapi = json.loads(html)
                            data=proxyapi['data']
                            self.proxies = {}
                            for one in data:
                                ip_port=one['proxy'].strip('http://')
                                proxy_address='http://%s' % (ip_port)
                                if ip_port:
                                    self.proxies[proxy_address]=ip_port
                    except Exception,e:
                        sleep(60)
                        continue

                    if len(self.proxies)>0:
                        break
                    else:
                        sleep(60)

        # Don't overwrite with a random one (server-side state for IP)
        #if 'proxy' in request.meta:
         #   return
        while True:
            try:
                proxy_address = random.choice(self.proxies.keys())
                if proxy_address:
                    break
            except KeyError and IndexError and Exception,e:
                pass
        #proxy_user_pass = self.proxies[proxy_address]
        request.meta['proxy'] =proxy_address

    def process_exception(self, request, exception, spider):
        #log.msg('Removing failed proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))

        try:
            proxy_address = request.meta['proxy']

            print '++++++++++'+proxy_address+'++++++++++',len(self.proxies)
            if self.proxies.has_key(proxy_address)and len(self.proxies)>5:
                del self.proxies[proxy_address]
        except KeyError and IndexError and Exception,e:
            pass

