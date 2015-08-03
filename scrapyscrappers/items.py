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
    
    item_url = scrapy.Field(default='')
    title = scrapy.Field(default='')
    description = scrapy.Field(default='')
    short_description = scrapy.Field(default='')
    company = scrapy.Field(default='')
    department = scrapy.Field(default='')
    locality = scrapy.Field(default='')
    region = scrapy.Field(default='')
    published = scrapy.Field(default='')
    salary = scrapy.Field(default='')
    clearance = scrapy.Field(default='')

    keyword = scrapy.Field()
    location_search = scrapy.Field()
    date_search = scrapy.Field()
