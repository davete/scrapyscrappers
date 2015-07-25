# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import bs4
from datetime import datetime

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  datetime2datetimestr

class ClearancejobsSpider(Spider):
    name = "clearancejobs"
    allowed_domains = ["www.clearancejobs.com"]
    base_url = 'https://www.clearancejobs.com'
    query_url = 'https://www.clearancejobs.com/jobs?RC=25&Ns=p_TimeStamp|1&Ntt=%(keyword)s&Ntk=IMain&Ntx=mode+matchall'
    # FIXME:
    #https://www.clearancejobs.com/jobs
    #https://www.clearancejobs.com/jobs?RC=25&Ns=p_TimeStamp|1&Ntt=software&Ntk=IMain&Ntx=mode+matchall
    #https://www.clearancejobs.com/jobs?Ntx=mode+matchall&Ntk=IMain&RC=25&Ns=p_TimeStamp|1&Ntt=engineer
    #https://www.clearancejobs.com/jobs?Ntx=mode+matchall&Ntk=IMain&RC=25&Ns=p_TimeStamp|1&Ntt=python&No=25

    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
        # to call the spider with keywords and locations arguments
        super(ClearancejobsSpider, self).__init__(*args, **kwargs)
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
        item['description'] =  response.css('.cj-job-details').extract()[0] #div
        yield item

    def parse(self, response):
        self.logger.debug('parsing')
        results = response.css('#search-results') # div
        rows = results.css('.cj-search-result-item')
        for row in rows:
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            item['title'] = row.xpath('.//strong[@class="cj-search-result-item-title"]/a/text()').extract()[0].strip()
            item['item_url'] = row.xpath('.//strong[@class="cj-search-result-item-title"]/a/@href').extract()[0]
            item['short_description'] = ''
            item['company'] = row.xpath('.//span[@class="cj-company-name"]/a/text()').extract()[0].strip()
            #location = row.xpath('.//span[@class="cj-company-name"]/text()').extract()[0].strip()
            location = row.css('.cj-job-primary-info::text').extract()[1].strip()
            try:
                item['locality'] ,  item['region']  = location.split(', ')
            except ValueError:
                item['locality'] = loc
                item['region'] = ''
            item['salary'] = ''
            item['department'] = ''
            #updated = row.css('.cj-text-sm::text').extract()[1].strip()
            updated = row.xpath('.//span[@class="cj-text-sm cj-color-mediumgray"]//text()').extract()[1].strip()
            try:
                dt = datetime.strptime(updated, '%m/%d/%y')
            # FIXME: check if exception not only cause of Today string but other string like yesterday
            except ValueError:
                dt = datetime.now()
            item['published'] = datetime2datetimestr(dt)
            #item['clearance'] = row.xpath('.//div[@class="cj-card-data"])').extract()[0].strip()
            item['clearance'] = row.css('.cj-card-data::text').extract()[1]
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        #FIXME: no a link, javascript
        next = response.xpath('button[@class="cj-table-pagination-next"]/a/@href').extract()
        if next:
            self.logger.debug('next url: %s' % next[0] )
            yield Request(next[0],  callback=self.parse,  meta={'item': item})
            
