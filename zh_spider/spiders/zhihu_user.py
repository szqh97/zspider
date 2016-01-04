# -*- coding: utf-8 -*-
"""
TODO
"""
import os
import scrapy
import json
import time
from scrapy.http.request import Request

class  ZhihuUserSpider(scrapy.Spider):
    """
    This is a zhihu user crawler spider
    """
    name = "zhihu_user"
    allowed_domains = ["https://zhihu.com"]

    start_urls = (
        'https://www.zhihu.com/people/excited-vczh',
        #'https://www.zhihu.com/people/excited-vczh',
        'https://www.zhihu.com/people/cao-miao-miao-26',
    )

    followees = {}

    meta = {
           'dont_merge_cookies': True,
           'dont_redirect': True,
           'handle_httpstatus_list': [302]
           }

    def start_requests(self):
        for url in self.start_urls:
            followees_url = os.path.join(url, 'followees')
            self.logger.info("followees url is %s", url)
            yield Request(followees_url, meta=self.meta, callback=self.parse_followees_request)

            followers_url = os.path.join(url, 'followers')
            self.logger.info('followers url is {0}'.format(followers_url))
            yield Request(followers_url, meta=self.meta, callback=self.parse_followers_request)


    def parse_followers_request(self, response):
        pass

    def parse(self, response):
        pass

    def parse_followees_request(self, response):
        user_page = response.xpath('//div[@class="title-section ellipsis"]/a').xpath('@href').extract()[0]
        _xsrf = response.xpath('//input[@name="_xsrf"]').xpath("@value").extract()[0]
        self.logger.debug("xsrf is %s", _xsrf)
        str_curr_person_info = response.xpath('//script[@data-name="current_people"]/text()').extract()[0]
        hash_id = json.loads(str_curr_person_info)[-1]
        followees_xpth_herf = os.path.join(user_page, 'followees')
        followers_xpth_herf = os.path.join(user_page, 'followers')
        followees_number = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@href="{0}"]/strong/text()'.format(followees_xpth_herf)).extract()[0]
        followers_number = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@href="{0}"]/strong/text()'.format(followers_xpth_herf)).extract()[0]

        self.logger.debug("hash_id is %s", hash_id)

        # get top 20 followees
        user_info = {
                'user_page': user_page,
                'xsrf': _xsrf,
                'hash_id': hash_id,
                'followees': [],
                'followees_number': int(followees_number),
                'followers': [],
                'followers_number': int(followers_number),
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                }

        for p in response.xpath('//h2[@class="zm-list-content-title"]/a'):
            followee = {}
            followee['page_url'] = p.xpath('@href').extract()[0]
            followee['name'] = p.xpath('text()').extract()[0]
            followee['zhihu_id'] = p.xpath('@data-tip').extract()[0].split('p$t$')[-1]
            user_info['followees'].append(followee)


        return user_info

