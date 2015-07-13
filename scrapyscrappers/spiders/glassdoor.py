# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import re
from datetime import datetime

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  timeago2datetimestr


class GlassdoorSpider(Spider):
    name = "glassdoor"
    # FIXME: check other domains 
    #allowed_domains = ["glassdoor.com"]
    base_url = 'http://glassdoor.com'
    query_url = 'http://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=%(keyword)s&sc.keyword=%(keyword)s&locT=&locId=&jobType=all'
                         #http://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=python+ruby&sc.keyword=python+ruby&locT=C&locId=1147401&jobType=all
    # keywords are separated by +
    # FIXME: with location
    # location use self state code and self id
    
    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
        # to call the spider with keywords and locations arguments
        super(GlassdoorSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords or obtain_keywords()
        self.locations = locations or obtain_locations()

    def start_requests(self):
        self.logger.debug('in start requests')
        for location in self.locations:
            for keyword in self.keywords:
                url_params = {'keyword': keyword,  'location': location}
                url = self.query_url % url_params
                self.logger.debug('request url %s' % url)
                yield Request(url, meta={'keyword': keyword})
                
    def parse_item(self,  response):
        self.logger.debug('parse_item %s' % response.url)
        item = response.meta['item'] 
        # items are in different domains, store al page
        if not response.url.startswith(self.base_url):
            item['description'] = response.body
        yield item

    def parse(self, response):
        if response.status == 403:
            self.logger.debug('!!!!!!!!!! 403 from %s' % response.url)
        list = response.css('.standardJobListings')
        rows = list.xpath('.//div[@itemtype="http://schema.org/JobPosting"]')

        for row in rows:
            self.logger.debug('parsing')
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            
            url = row.xpath('.//h3[@itemprop="title"]/a/@href').extract()[0]
            item['item_url'] = self.base_url + url
            
            # a text could have span tag inside
            item['title'] = row.xpath('string(.//h3[@itemprop="title"]/a)').extract()[0].strip()
            
            item['company'] = row.xpath('string(.//span[@class="employerName"])').extract()[0].strip()
            
            published = row.css('.logo').css('.minor::text').extract()[0].strip()
            item['published'] =  timeago2datetimestr(item['date_search'],  published)
            
            item['short_description'] = row.xpath('string(.//p[@itemprop="description"])').extract()[0].strip()
            
            loc = row.xpath('string(.//span[@itemprop="addressLocality"])').extract()[0].strip()
            try:
                item['locality'] ,  item['region']  = loc.split(', ')
            except ValueError:
                item['locality'] = loc
                item['region'] = ''
                
            item['salary'] = ''
            item['clearance'] = ''
            item['department'] = ''
            item['description'] = ''
            self.logger.debug('title %s' % item['title'])
            #yield item
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.next a::attr(href)').extract()
        if next:
            self.logger.debug('next url: %s' % next[0] )
            yield Request(self.base_url + next[0],  callback=self.parse, meta={'keyword': response.meta['keyword']})


