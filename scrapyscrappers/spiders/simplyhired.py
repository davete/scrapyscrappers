# -*- coding: utf-8 -*-
from scrapy import Request

import bs4

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import datetimestr2datetime,  datetime2datetimestr, \
    timeago2datetimestr,  append


class SimplyhiredSpider(BaseSpider):
    name = "simplyhired"
    allowed_domains = ["www.simplyhired.com"]
    base_url = 'www.simplyhired.com'
    query_url = 'https://www.simplyhired.com/search?q=%(keyword)s&l=%(location)s'
    # next page
    # http://www.simplyhired.com/search?q=python+django&pn=2

    def parse_item(self,  response):
        item = super(SimplyhiredSpider, self).parse_item(response)
        try:
            item['description'] = response.css('div.detail')[0].extract()
            #item['description'] = response.css('div.description-full::text')[0].extract()
        except IndexError:
            append(self.fail_url_path, 'failed to parse:' + response.url)
        yield item


    def parse(self, response):
        super(SimplyhiredSpider,  self).parse(response)
#        # with scrapy selector
#        # for sel in response.xpath('//div[@class="job"]'):
#        for sel in response.css('div.job'):
#            item = self.init_item(response)
#            item['keyword'] = response.meta['keyword']
#            item['date_search'] = current_datetime()
#            #this works, but return different url
#            #item['item_url'] = sel.css('a.title::attr(href)').extract()[0]
#            item['item_url'] =[tool.css('a::attr(href)')[0].extract() for tool in sel.css('div.tools')][0]
#            item['title'] = sel.css('a.title::text').extract()[0].strip()

        # with bs4
        soup = bs4.BeautifulSoup(response.body)
        soupitems = soup.select('div.job')     
        if len(soupitems) < 1:
            append(self.fail_url_path, 'no data:' + response.url)
            return
        for soupitem in soupitems:
            item = self.init_item(response)
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
            # data not available in this website
            item['salary'] = ''
            item['clearance'] = ''
            item['department'] = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )

        #for url in response.xpath('//link[@rel="next"]/@href').extract()[0]:
        next = response.css('a.next::attr(href)').extract()            
        if next:
            self.logger.debug('next url: %s' % next[0])
            yield Request(
                # self.base_url + next[0]['href'],  # with soup
                next[0], 
                callback=self.parse, 
                meta={'keyword': response.meta['keyword'],  'location': response.meta['location']}
            )
        else:
            self.logger.debug('no next url')            
