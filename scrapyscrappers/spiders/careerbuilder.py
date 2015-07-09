# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import bs4

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime

class CareerbuilderSpider(Spider):
    name = "careerbuilder"
    allowed_domains = ["www.careerbuilder.com"]
    base_url = 'https://www.careerbuilder.com'
    query_url = 'https://www.careerbuilder.com/jobseeker/jobs/jobresults.aspx?s_rawwords=%(keyword)s&s_freeloc=%(location)s'


    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
        # to call the spider with keywords and locations arguments
        super(CareerbuilderSpider, self).__init__(*args, **kwargs)
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
        #soup = bs4.BeautifulSoup(response.body)     
        item['title'] = response.xpath('//h1/span/text()').extract()
        item['description'] = ''
        item['clearance'] = ''
        self.logger.debug('title item %s' % item['title'])
        yield item

    def parse(self, response):
#        itemscopes_ = response.xpath('//table[@itemscope]')
#        for itemscope in itemscopes:
        table = response.css('.gs-job-result-abstract')
        for row in table:
            #self.logger.debug('parsing')
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            item['item_url'] = row.css('.jt').xpath('@href').extract()[0]
            item['title'] = row.css('.jt::text').extract()
            item['short_description'] = ''
            item['company'] = ''
            item['locality'] = ''
            item['region'] = ''
            item['salary'] = ''
            item['department'] = ''
            item['published'] = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.JL_MXDLPagination2_next').xpath('@href').extract()
        # FIXME: uncomment
        if next:
            self.logger.debug('next url: %s' % next[0] )
            # FIXME: the request seems not being called
            yield Request(next[0],  callback=self.parse)
