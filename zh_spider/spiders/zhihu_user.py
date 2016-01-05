# -*- coding: utf-8 -*-
"""
TODO
"""
import os
import scrapy
import json
import time
import bs4.BeautifulSoup
import traceback
import httplib2
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
        try:
            user_page = response.xpath('//a[@class="name"]').xpath('@href').extract()[0]
            user_info['user_page'] = user_page
            str_curr_person_info = response.xpath('//script[@data-name="current_people"]/text()').extract()[0]
            hash_id = json.loads(str_curr_person_info)[-1]
            user_info['hash_id'] = hash_id
        except Exception, e:
            self.logger.error('{0}'.format(traceback.format_exc()))

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
        user_info = {}
        user_page = response.xpath('//div[@class="title-section ellipsis"]/a').xpath('@href').extract()[0]
        user_info['user_page'] = user_page
        zhihu_id = user_page.split('/')[-1]
        str_curr_person_info = response.xpath('//script[@data-name="current_people"]/text()').extract()[0]
        hash_id = json.loads(str_curr_person_info)[-1]
        followers_xpth_herf = os.path.join(user_page, 'followers')
        followers_number = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@href="{0}"]/strong/text()'.format(followers_xpth_herf)).extract()[0]
        user_info_followers = {
                'zhihu_id': zhihu_id,
                'user_page': user_page,
                'followers_number': int(followers_number),
                'followers': [],
                'hash_id': hash_id
                }

        for p in response.xpath('//h2[@class="zm-list-content-title"]/a'):
            followee = {}
            followee['page_url'] = p.xpath('@href').extract()[0]
            followee['name'] = p.xpath('text()').extract()[0]
            followee['zhihu_id'] = p.xpath('@data-tip').extract()[0].split('p$t$')[-1]
            user_info_followers['followers'].append(followee)

        yield user_info_followers


    def parse_followees_request(self, response):
        user_page = response.xpath('//div[@class="title-section ellipsis"]/a').xpath('@href').extract()[0]
        zhihu_id = user_page.split('/')[-1]
        _xsrf = response.xpath('//input[@name="_xsrf"]').xpath("@value").extract()[0]
        self.logger.debug("xsrf is %s", _xsrf)
        str_curr_person_info = response.xpath('//script[@data-name="current_people"]/text()').extract()[0]
        hash_id = json.loads(str_curr_person_info)[-1]
        followees_xpth_herf = os.path.join(user_page, 'followees')
        followees_number = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@href="{0}"]/strong/text()'.format(followees_xpth_herf)).extract()[0]

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
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                }

        for p in response.xpath('//h2[@class="zm-list-content-title"]/a'):
            followee = {}
            followee['page_url'] = p.xpath('@href').extract()[0]
            followee['name'] = p.xpath('text()').extract()[0]
            followee['zhihu_id'] = p.xpath('@data-tip').extract()[0].split('p$t$')[-1]
            user_info['followees'].append(followee)

        yield user_info

    def parse_all_followees(self, user_page, offset, hash_id, xsrf):
        """ 
        parse all followees
        TODO: may be use scrapy http request lib to rewrite it
        FIXME: add Exception deal
        """
        cookie = '_za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390'
        followee_headers = {
             'Host' : 'www.zhihu.com',
             'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',
             'Accept' : '*/*',
             'Accept-Language' : 'en-US,en;q=0.5',
             'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
             'X-Requested-With' : 'XMLHttpRequest',
             'Referer' : 'https://www.zhihu.com/people/excited-vczh/followees',
             'Cookie' : cookie,
             'Connection' : 'keep-alive',
             'Pragma' : 'no-cache',
             'Cache-Control' : 'no-cache',
        }

        ProfileFolloweesListV2_url = 'https://www.zhihu.com/node/ProfileFolloweesListV2'
        data='method=next&params=%7B%22offset%22%3A{0}%2C%22order_by%22%3A%22created%22%2C%22hash_id%22%3A%22{1}%22%7D&_xsrf={2}'.format(offset, hash_id, xsrf)
        try:
            http = httplib2.Http(disable_ssl_certificate_validation=False)
            resp, content = http.request(ProfileFolloweesListV2_url, method='POST', headers=followee_headers, body=data)
        except Exception, e:
            self.logger.error('{0}'.format(traceback.format_exc()))
        else:
            if resp.status == 200 :
                content_obj = json.loads(context)
                if len(content_obj['msg']) != 0:
                    for user_html in content_obj['msg']:
                        soup = bs4.BeautifulSoup(user_html)
                        h2 = soup.find('h2')
                        name = h2.getText()
                        user_url = h2.find('a')['href']
                        title = soup.find('div', {'class':'zg-big-gray'}).getText()














