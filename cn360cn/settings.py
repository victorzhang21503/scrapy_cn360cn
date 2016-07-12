# Scrapy settings for yellowpages project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cn360cn'

#BOT_VERSION = '1.0'

SPIDER_MODULES = ['cn360cn.spiders']
NEWSPIDER_MODULE = 'cn360cn.spiders'




ITEM_PIPELINES = {
   BOT_NAME+'.pipelines.'+BOT_NAME.capitalize()+'Pipeline': 300,
}
COOKIES_ENABLED=False
DOWNLOAD_TIMEOUT=3
CONCURRENT_REQUESTS=1
DOWNLOAD_DELAY = 0.1
RANDOMIZE_DOWNLOAD_DELAY = True
CRAWLERA_ENABLED = True
CRAWLERA_USER = 'e19285de140b4a6ca70ea0b347b2a404'
CRAWLERA_PASS = 'Victor@78945612'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

USER_AGENT ='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
# Retry many times since proxies often fail
RETRY_TIMES =50
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500,501,502, 503, 504,505,506,507,508,509, 400,401,402, 403, 404,405,406, 407, 408,409, 301, 302, 303,304,305,306, 307,308,309]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    #'scrapy_crawlera.CrawleraMiddleware': 600,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #BOT_NAME+'.middlewares.ProxyMiddleware': 100,
}

#CON='conf.txt'
