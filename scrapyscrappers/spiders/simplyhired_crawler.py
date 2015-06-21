# -*- coding: utf-8 -*-
import scrapy
from scrapy import log,  Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 

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
                  Rule (SgmlLinkExtractor(restrict_xpaths=('//a[@class="next"]',)) , follow= True ), 
        )
        
    def __init__(self, keywords="", locations="",  *args, **kwargs):
        log.msg('in init', log_level=log.DEBUG)
        # to call the spider with keywords and locations arguments
        super(SimplyhiredCrawler, self).__init__(*args, **kwargs)
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
        try:
            # log.msg('extracting descrption', log_level=log.DEBUG)
            item['description'] = response.css('div.detail')[0].extract()
            #item['description'] = response.css('div.description-full::text')[0].extract()
        except:
            #log.msg(response.css('div.description-full::text'), log_level=log.DEBUG)
            log.msg('error parsing description', log_level=log.DEBUG)
#        item['clearance'] = infodict.get('SECURITY CLEARANCE')
        yield item            

                
    def parse(self, response):
        log.msg('in parse', log_level=log.DEBUG)
#        # for sel in response.xpath('//div[@class="job"]'):
#        for sel in response.css('div.job'):
#            log.msg('parsing', log_level=log.DEBUG)
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
            log.msg('parsing', log_level=log.DEBUG)
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
            
            log.msg('title %s' % item['title'], log_level=log.DEBUG)
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
    
