# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 

import bs4

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  table2dict


class UsajobsCrawler(CrawlSpider):
    name = "usajobscrawler"
    allowed_domains = ["www.usajobs.gov"]
    base_url = 'https://www.usajobs.gov'
    query_url = 'https://www.usajobs.gov/Search?Keyword=%(keyword)s&Location=%(location)s&search=Search&AutoCompleteSelected=False'
    rules = [
             # not using this rule to parse items from the list
             #Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="jobResultNew"]//a[@class="jobTitleLink"]')), callback='parse_item'), 
             Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="resultspager-middle"]//a[@class="nextPage"]')), follow=True)
             ]

    def __init__(self, keywords="", locations="",  *args, **kwargs):
        log.msg('in init', log_level=log.DEBUG)
        # to call the spider with keywords and locations arguments
        super(UsajobsCrawler, self).__init__(*args, **kwargs)
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
        # FIXME: uncomment when not debugging
        #item['description'] = soup.select('div.jobdetail')[0].text
        infodict = table2dict(soup,  'div#jobinfo2')
        item['clearance'] = infodict.get('SECURITY CLEARANCE')
        yield item

    def parse(self, response):
        log.msg('in parse', log_level=log.DEBUG)
        soup = bs4.BeautifulSoup(response.body)
        soupitems = soup.select('div#jobResultNew')    
        for soupitem in soupitems:
            item = ScrapyscrappersItem()
            item['keyword'] = response.meta['keyword']
            item['date_search'] = current_datetime()
            item['item_url'] = self.base_url + soupitem.select('a.jobTitleLink')[0].attrs.get('href')
            item['title'] = soupitem.select('a.jobTitleLink')[0].text
            item['short_description'] = soupitem.select('p.summary')[0].text.strip()
            details = table2dict(soupitem,  'table.joaResultsDetailsTable')
            item['company'] = details.get('Agency',  '')
            location_region = details.get('Location(s)',  '').split(', ')
            item['locality'] = location_region[0]
            try:
                item['region'] = location_region[1]
            except IndexError:
                pass
            item['salary'] = details.get('Salary',  '')
            item['department'] = details.get('Department',  '')
            # item.published = ''
            log.msg('title %s' % item['title'], log_level=log.DEBUG)
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
