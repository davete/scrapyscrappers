# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import bs4

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  timeago2datetimestr
# FIXME: get settings properly
# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()
#from scrapyscrappers.settings import DEBUG

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
        #item['title'] = response.xpath('//h1/span/text()').extract()
        #if DEBUG == False:
        #item['description'] = response.css('article').extract()
        # or
        item['description'] = response.xpath('//article').extract()[0]
        # or to dont get html tags
        #item['description'] = bs4.BeautifulSoup(response.body).select('article')[0].text
        item['clearance'] = ''
        self.logger.debug('title item %s' % item['title'])
        yield item

    def parse(self, response):
        table = response.css('.gs-job-result-abstract')
        for row in table:
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            item['item_url'] = row.css('.jt').xpath('@href').extract()[0]
            item['title'] = row.css('.jt::text').extract()[0]
            #item['short_description'] = row.css('span[itemprop="description"]::text').extract()[0]
            # the same with xpath
            item['short_description'] = row.xpath('.//span[@itemprop="description"]/text()').extract()[0]
            item['company'] = row.xpath('.//a/@companyname').extract()[0]
            # or
#            try:
#                item['company'] = row.xpath('.//td[@itemprop="hiringOrganization"]/a/text()').extract()[0]
#            except IndexError:
#                self.logger.debug(row.xpath('.//td[@itemprop="hiringOrganization"]/a/text()').extract())
            location = row.xpath('.//div[@itemprop="jobLocation"]/span/text()').extract()[0]
            try:
                item['region'] ,  item['locality'] = location.split(' - ')
            except ValueError:
                item['locality'] = location
            teaser = [i.strip() for i in row.xpath('.//div[contains(@id, "pnlTeaser")]/p/text()').extract()[0].split('|')]
            if len(teaser) == 2:
                item['salary'] = teaser[1].split(':')[1]
            else:
                item['salary'] = ''
            item['department'] = ''
            ago = row.css('.jl_rslt_posted_cell span::text').extract()[0]
            item['published'] = timeago2datetimestr(item['date_search'] , ago)
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.JL_MXDLPagination2_next').xpath('@href').extract()
        if next:
            self.logger.debug('next url: %s' % next[0] )
            yield Request(next[0],  callback=self.parse, meta={'keyword': response.meta['keyword']})
