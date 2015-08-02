# -*- coding: utf-8 -*-
from scrapy.http import Request

import bs4

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import table2dict
    
class UsajobsSpider(BaseSpider):
    name = "usajobsspider"
    allowed_domains = ["www.usajobs.gov"]
    base_url = 'https://www.usajobs.gov'
    query_url = 'https://www.usajobs.gov/Search?Keyword=%(keyword)s&Location=%(location)s&search=Search&AutoCompleteSelected=False'


    def parse_item(self,  response):
        item = super(UsajobsSpider, self).parse_item(response)
        soup = bs4.BeautifulSoup(response.body)          
        item['description'] = soup.select('div.jobdetail')[0].text
        infodict = table2dict(soup,  'div#jobinfo2')
        item['clearance'] = infodict.get('SECURITY CLEARANCE')
        yield item


    def parse(self, response):
        super(UsajobsSpider,  self).parse(response)
        soup = bs4.BeautifulSoup(response.body)
        soupitems = soup.select('div#jobResultNew')    
        for soupitem in soupitems:
            item = self.init_item(response)
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
