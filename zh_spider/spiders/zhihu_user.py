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

    meta = {
           'dont_merge_cookies': True,
           'dont_redirect': True,
           'handle_httpstatus_list': [302]
           }
    def start_requests(self):
        for url in self.start_urls:
            self.logger.info("start url is %s", url)
            #yield Request(url, headers=self.headers, meta=self.meta, callback=self.parse_followee_request)
            yield Request(url, meta=self.meta, callback=self.parse_followee_request)

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


