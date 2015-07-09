# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import bs4

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  current_datetime,  table2dict
    
class UsajobsSpider(Spider):
    name = "usajobsspider"
    allowed_domains = ["www.usajobs.gov"]
    base_url = 'https://www.usajobs.gov'
    query_url = 'https://www.usajobs.gov/Search?Keyword=%(keyword)s&Location=%(location)s&search=Search&AutoCompleteSelected=False'


    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
        # to call the spider with keywords and locations arguments
        super(UsajobsSpider, self).__init__(*args, **kwargs)
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
        soup = bs4.BeautifulSoup(response.body)          
        # FIXME: uncomment when not debugging
        #item['description'] = soup.select('div.jobdetail')[0].text
        infodict = table2dict(soup,  'div#jobinfo2')
        item['clearance'] = infodict.get('SECURITY CLEARANCE')
        yield item

    def parse(self, response):
        self.logger.debug('in parse')
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
            # data not available in this website
            # item.published = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = soup.select('a.nextPage')
        if next:
            self.logger.debug('next url: %s' % url )
            yield Request(self.base_url + next[0]['href'],  callback=self.parse, meta={'keyword': response.meta['keyword']})
