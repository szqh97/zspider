# -*- coding: utf-8 -*-

# Scrapy settings for zh_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zh_spider'

SPIDER_MODULES = ['zh_spider.spiders']
NEWSPIDER_MODULE = 'zh_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zh_spider (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

cookie = '_za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390'
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.zhihu.com/people/excited-vczh/followees',
    'Cookie': cookie,
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'


}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zh_spider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zh_spider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'zh_spider.pipelines.SomePipeline': 300,
    'zh_spider.pipelines.ZhSpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
