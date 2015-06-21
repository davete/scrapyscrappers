# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyscrappersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    
    item_url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    short_description = scrapy.Field()
    company = scrapy.Field()
    department = scrapy.Field()
    locality = scrapy.Field()
    region = scrapy.Field()
    published = scrapy.Field()
    salary = scrapy.Field()
    clearance = scrapy.Field()
    
#    base_url = scrapy.Field()
    keyword = scrapy.Field()
    date_search = scrapy.Field()
