# -*- coding: utf-8 -*-
"""
TODO
"""
import scrapy
import json
from scrapy.http.request import Request

class  ZhihuUserSpider(scrapy.Spider):
    """
    This is a zhihu user crawler spider
    """
    name = "zhihu_user"
    allowed_domains = ["https://zhihu.com"]

    #FIXME start_urls and cookie should passed 
    start_urls = (
        'https://www.zhihu.com/people/excited-vczh/followees',
        #'https://www.zhihu.com/people/excited-vczh',
        'https://www.zhihu.com/people/cao-miao-miao-26/followees',
    )

    followees = {}

    cookie = '_za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390'
 
    headers = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            #'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.zhihu.com/people/excited-vczh/followees',
            'Cookie': cookie,
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
            }


    meta = {
           'dont_merge_cookies': True,
           'dont_redirect': True,
           'handle_httpstatus_list': [302]
           }
    def start_requests(self):
        for url in self.start_urls:
            self.logger.info("start url is %s", url)
            yield Request(url, headers=self.headers, meta=self.meta, callback=self.parse_followee_request)


    def parse(self, response):
        pass

    def parse_followee_request(self, response):
        #self.logger.debug("self.body is %s", response.body)

        # get xsrf for next request
        user_page = response.xpath('//div[@class="title-section ellipsis"]/a').xpath('@href').extract()[0]
        self._xsrf = response.xpath('//input[@name="_xsrf"]').xpath("@value").extract()[0]
        self.logger.debug("xsrf is %s", self._xsrf)
        str_curr_person_info = response.xpath('//script[@data-name="current_people"]/text()').extract()[0]
        self.hash_id = json.loads(str_curr_person_info)[-1]
        self.logger.debug("hash_id is %s", self.hash_id)

        # get top 20 followees
        tmp_followees = {user_page: []}

        for p in response.xpath('//h2[@class="zm-list-content-title"]/a'):
            followee = {}
            followee['page_url'] = p.xpath('@href').extract()[0]
            followee['name'] = p.xpath('text()').extract()[0]
            followee['zhihu_id'] = p.xpath('@data-tip').extract()[0].split('p$t$')[-1]
            tmp_followees[user_page].append(followee)
            self.logger.debug("followee is %s", str(followee))

        return tmp_followees


