# -*- coding: utf-8 -*-
"""
TODO
"""
import os
import scrapy
import json
import time
import traceback
from scrapy.http.request import Request

class  ZhihuUserSpider(scrapy.Spider):
    """
    This is a zhihu user crawler spider
    """
    name = "zhihu_user"
    allowed_domains = ["https://zhihu.com"]

    start_urls = (
        'https://www.zhihu.com/people/excited-vczh',
        #'https://www.zhihu.com/people/cao-miao-miao-26',
    )

    followees = {}

    meta = {
           'dont_merge_cookies': True,
           'dont_redirect': True,
           'handle_httpstatus_list': [302]
           }

    def start_requests(self):
        for url in self.start_urls:
            about_url = os.path.join(url, 'about')
            self.logger.info('about url is {0}'.format(about_url))
            yield Request(about_url, meta=self.meta, callback=self.parse_about_request)

            followees_url = os.path.join(url, 'followees')
            self.logger.info("followees url is %s", followees_url)
            yield Request(followees_url, meta=self.meta, callback=self.parse_followees_request)

            followers_url = os.path.join(url, 'followers')
            self.logger.info('followers url is {0}'.format(followers_url))
            yield Request(followers_url, meta=self.meta, callback=self.parse_followers_request)


    def parse_about_request(self, response):

        user_info = {}
        # FIXME add hash_id or other
        user_page = response.xpath('//a[@class="name"]').xpath('@href').extract()[0]
        user_info['user_page'] = user_page
        try:
            user_weibo = response.xpath('//a[@class="zm-profile-header-user-weibo"]').xpath('@href').extract()[0]
            weibo_tip = response.xpath('//a[@class="zm-profile-header-user-weibo"]').xpath('@data-tip').extract()[0].split('s$b$')[-1]
        except Exception, e:
            self.logger.debug('user may not use weibo ...')
        else:
            user_info['user_weibo']     = user_weibo
            user_info['weibo_tip']      = weibo_tip

        try:  user_info['location'] = response.xpath('//span[@class="location item"]/a/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set location')

        try:  user_info['business'] = response.xpath('//span[@class="business item"]/a/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set business')

        try:  user_info['gender'] = response.xpath('//input[@checked="checked"]').xpath('@class').extract()[0]
        except Exception, e: self.logger.debug('user may not set gender !?')

        try:  user_info['employment'] = response.xpath('//span[@class="employment item"]/a/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set employment')

        try:  user_info['position'] = response.xpath('//span[@class="position item"]/a/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set position')

        try:  user_info['education'] = response.xpath('//span[@class="education item"]/a/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set education')

        try:  user_info['education-extra'] = response.xpath('//span[@class="education-extra item"]/a/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set education-extra')

        try:  user_info['description'] = response.xpath('//textarea/text()').extract()[0]
        except Exception, e: self.logger.debug('user may not set description')

        try:  user_info['agrees'] = int(response.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract()[0])
        except Exception, e: self.logger.debug('user may not agrees')

        try:  user_info['thanks'] = int(response.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract()[0])
        except Exception, e: self.logger.debug('user may not thanks')


        try:  
            ask_href = os.path.join(user_page, 'asks')
            user_info['asks'] = int(response.xpath('//span[@class="{0}"]/span/text()'.format(ask_href)).extract()[0])
        except Exception, e: self.logger.debug('user may not asks')

        try:  
            ask_href = os.path.join(user_page, 'answers')
            user_info['answers'] = int(response.xpath('//a[@href="{0}"]/span/text()'.format(ask_href)).extract()[0])
        except Exception, e: self.logger.debug('user may not answers')

        try:  
            ask_href = os.path.join(user_page, 'posts')
            user_info['posts'] = int(response.xpath('//a[@href="{0}"]/span/text()'.format(ask_href)).extract()[0])
        except Exception, e: self.logger.debug('user may not posts ')

        try:  
            ask_href = os.path.join(user_page, 'collections')
            user_info['collections'] = int(response.xpath('//a[@href="{0}"]/span/text()'.format(ask_href)).extract()[0])
        except Exception, e: self.logger.debug('user may not collections')

        try:  
            ask_href = os.path.join(user_page, 'logs')
            user_info['logs'] = int(response.xpath('//a[@href="{0}"]/span/text()'.format(ask_href)).extract()[0])
        except Exception, e: self.logger.debug('user may not logs')

        return user_info


    def parse_followers_request(self, response):
        user_page = response.xpath('//div[@class="title-section ellipsis"]/a').xpath('@href').extract()[0]
        zhihu_id = user_page.split('/')[-1]
        str_curr_person_info = response.xpath('//script[@data-name="current_people"]/text()').extract()[0]
        hash_id = json.loads(str_curr_person_info)[-1]
        followers_xpth_herf = os.path.join(user_page, 'followers')
        followers_number = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@href="{0}"]/strong/text()'.format(followers_xpth_herf)).extract()[0]
        user_info_followers = {
                'zhihu_id': zhihu_id,
                'followers_number': int(followers_number),
                'followers': []
                }

        for p in response.xpath('//h2[@class="zm-list-content-title"]/a'):
            followee = {}
            followee['page_url'] = p.xpath('@href').extract()[0]
            followee['name'] = p.xpath('text()').extract()[0]
            followee['zhihu_id'] = p.xpath('@data-tip').extract()[0].split('p$t$')[-1]
            user_info_followers['followers'].append(followee)

        return user_info_followers

    def parse_followees_request(self, response):
        user_page = response.xpath('//div[@class="title-section ellipsis"]/a').xpath('@href').extract()[0]
        zhihu_id = user_page.split('/')[-1]
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
                'zhihu_id': zhihu_id,
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

