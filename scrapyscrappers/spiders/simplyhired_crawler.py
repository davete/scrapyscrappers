# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor 

import bs4

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  \
    datetimestr2datetime,  datetime2datetimestr, timeago2datetimestr

class  SimplyhiredCrawler(CrawlSpider):
    name = "simplyhiredcrawler"
    allowed_domains = ["www.simplyhired.com"]
    base_url = 'https://www.simplyhired.com'
    query_url = 'https://www.simplyhired.com/search?q=%(keyword)s&l=%(location)s'
    rules = ( 
                  Rule (LinkExtractor(restrict_xpaths=('//a[@class="next"]',)) , follow= True ), 
        )
        
    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
        # to call the spider with keywords and locations arguments
        super(SimplyhiredCrawler, self).__init__(*args, **kwargs)
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
        try:
            # self.logger.debug('extracting descrption')
            item['description'] = response.css('div.detail')[0].extract()
            #item['description'] = response.css('div.description-full::text')[0].extract()
        except:
            #self.logger.debug(response.css('div.description-full::text'))
            self.logger.debug('error parsing description')
#        item['clearance'] = infodict.get('SECURITY CLEARANCE')
        yield item            

                
    def parse(self, response):
        self.logger.debug('in parse')
#        # for sel in response.xpath('//div[@class="job"]'):
#        for sel in response.css('div.job'):
#            self.logger.debug('parsing')
#            item = ScrapyscrappersItem()
#            item['keyword'] = response.meta['keyword']
#            item['date_search'] = current_datetime()
#            # item['item_url'] = sel.xpath('.//div[@class="tools"]/@href').extract()[0]
#            #item['item_url'] = sel.css('a.title::attr(href)').extract()[0]
#            item['item_url'] =[tool.css('a::attr(href)')[0].extract() for tool in sel.css('div.tools')][0]
#            #item['title'] = sel.xpaht('.//h2')
#            item['title'] = sel.css('a.title::text').extract()[0].strip()

        soup = bs4.BeautifulSoup(response.body)
        soupitems = soup.select('div.job')     
        for soupitem in soupitems:
            self.logger.debug('parsing')
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            item['item_url'] = [a.attrs.get('href') for a in soupitem.select('div.tools > a') if a.attrs.get('href')][0]
            item['title'] = soupitem.select('h2')[0].text.strip()
            try:
                item['company'] = soupitem.h4.text
            except AttributeError:
                pass
            #      logger.debug('item: %s has no h4 tag' % i)
            if soupitem.find('span', itemprop="addressLocality"):
                item['locality'] = soupitem.find('span', itemprop="addressLocality").text
            if soupitem.find('span', itemprop="addressRegion"):
                item['region'] = soupitem.find('span', itemprop="addressRegion").text
            item['short_description'] = soupitem.find('p', itemprop="description").text
            item['published'] = timeago2datetimestr(item['date_search'],  soupitem.select('span.ago')[0].text)
            #salary
            #clearance
            #department
            #description
            
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
    
