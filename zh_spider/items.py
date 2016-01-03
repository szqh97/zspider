# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class zhihuUserInfo (scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zhihu_id            = scrapy.Field()
    name                = scrapy.Field()
    hash_id             = scrapy.Field()
    bio                 = scrapy.Field()
    location            = scrapy.Field()
    business            = scrapy.Field()
    gender              = scrapy.Field()
    employment          = scrapy.Field()
    position            = scrapy.Field()
    education           = scrapy.Field()
    education-extra     = scrapy.Field()
    asks                = scrapy.Field()
    answers             = scrapy.Field()
    posts               = scrapy.Field()
    collections         = scrapy.Field()
    logs                = scrapy.Field()
    votes               = scrapy.Field()
    tanks               = scrapy.Field()
    favors              = scrapy.Field()
    shares              = scrapy.Field()
    followees           = scrapy.Field()
    followers           = scrapy.Field()
    pass
