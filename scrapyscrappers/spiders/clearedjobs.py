# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import re
from datetime import datetime

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  datetime2datetimestr


class ClearedjobsSpider(Spider):
    name = "clearedjobs"
    allowed_domains = ["clearedjobs.net"]
    base_url = 'http://clearedjobs.net'
    query_url = 'http://clearedjobs.net/index.php?action=advanced_search&page=search&zip_radius=20&keywords=%(keyword)s&city_state_zip=%(location)s&security_clearance=&submit=SEARCH+JOBS'
    # keywords are separated by +
    
    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
        # to call the spider with keywords and locations arguments
        super(ClearedjobsSpider, self).__init__(*args, **kwargs)
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
        item['description'] = response.css('.view_long').extract()[0]

        item['salary'] = response.css('.view_job').xpath('.//div//div[contains(.,"Salary:")]/following-sibling::div[1]/text()').extract()[0].strip()
        yield item

    def parse(self, response):
        table = response.xpath('//table[@class="search_res"]//tbody')
        rows = table.xpath('.//tr')

        for row in rows:
            self.logger.debug('parsing')
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            
            cols = row.xpath('.//td')
            col0 = cols[0]
            url = col0.xpath('.//a[@class="search"]/@href').extract()[0]
            item['item_url'] = self.base_url + "/" + url
            
            # a text could have span tag inside
            item['title'] = col0.xpath('string(.//a[@class="search"])').extract()[0].strip()
            
            item['company'] = col0.xpath('.//div[@class="info"]//a/text()').extract()[0]
            try:
                item['clearance'] = col0.xpath('.//div[@class="desc"]/text()').extract()[0]
            except IndexError:
                item['clearance'] = ''
            
            published = col0.xpath('.//div[@class=""]/text()').extract()[0].replace('Posted - ','')
            item['published'] = datetime2datetimestr(datetime.strptime(u'July 8, 2015', '%B %d, %Y'))
            
            item['short_description'] = ''
            
            col1 = cols[1]
            loc = col1.xpath('./text()').extract()[0].strip()
            try:
                item['locality'] ,  item['region']  = loc.split(', ')
            except ValueError:
                item['locality'] = loc
                item['region'] = ''
                
            item['salary'] = ''
            item['department'] = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.navbar_bottom').xpath('.//a[text()=">"]/@href').extract()
        if next:
            self.logger.debug('next url: %s' % next[0] )
            if next[0].startswith('/'):
                yield Request(self.base_url + next[0],  callback=self.parse, meta={'keyword': response.meta['keyword']})
            else:
                yield Request(self.base_url + '/' + next[0],  callback=self.parse, meta={'keyword': response.meta['keyword']})


