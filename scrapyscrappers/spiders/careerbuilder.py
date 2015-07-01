# -*- coding: utf-8 -*-
from scrapy import log,  Spider
from scrapy.http import Request

import bs4

from scrapyscrappers.items import ScrapyscrappersItem

class CareerbuilderSpider(Spider):
    name = "careerbuilder"
    allowed_domains = ["www.careerbuilder.com"]
    base_url = 'https://www.careerbuilder.com'
    query_url = 'https://www.careerbuilder.com/jobseeker/jobs/jobresults.aspx?s_rawwords=%(keyword)s&s_freeloc=%(location)s'


    def __init__(self, keywords="", locations="",  *args, **kwargs):
        log.msg('in init', log_level=log.DEBUG)
        # to call the spider with keywords and locations arguments
        super(CareerbuilderSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords or obtain_keywords()
        self.locations = locations or obtain_locations()

    def start_requests(self):
        log.msg('in start requests', log_level=log.DEBUG)
        for location in self.locations:
            for keyword in self.keywords:
                url_params = {'keyword': keyword,  'location': location}
                url = self.query_url % url_params
                log.msg('request url %s' % url, log_level=log.DEBUG)
                yield Request(url, meta={'keyword': keyword})
                
    def parse_item(self,  response):
        log.msg('parse_item %s' % response.url, log_level=log.DEBUG)
        item = response.meta['item']
        soup = bs4.BeautifulSoup(response.body)          
        item['description'] = soup.select('')[0].text
        item['clearance'] = ''
        yield item

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.body)
        soupitems = soup.select('')    
        for soupitem in soupitems:
            log.msg('parsing', log_level=log.DEBUG)
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            item['item_url'] = self.base_url + soupitem.select('')[0].attrs.get('href')
            item['title'] = soupitem.select('')[0].text
            item['short_description'] = soupitem.select('')[0].text.strip()
            item['company'] = ''
            item['locality'] = ''
            item['region'] = ''
            item['salary'] = ''
            item['department'] = ''
            item['published'] = ''
            log.msg('title %s' % item['title'], log_level=log.DEBUG)
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        #next = soup.select('a.jt.prefTitle')
        #next = soup.select('td.bottom-pagination')
        # is JL_MXDLPagination2_next constant or changes
        response.xpath('.//td[@class="bottom-pagination"]//a[@class="JL_MXDLPagination2_next"]/@href').extract()[0]
        if next:
            log.msg('next url: %s' % next[0],  log_level=log.DEBUG )
            yield Request(self.base_url + next[0]['href'],  callback=self.parse)
