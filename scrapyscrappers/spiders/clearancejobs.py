# -*- coding: utf-8 -*-
from scrapy.http import Request

from datetime import datetime

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import datetime2datetimestr

class ClearancejobsSpider(BaseSpider):
    name = "clearancejobs"
    allowed_domains = ["www.clearancejobs.com"]
    base_url = 'https://www.clearancejobs.com'
    query_url = 'https://www.clearancejobs.com/jobs?RC=25&Ns=p_TimeStamp|1&Ntt=%(keyword)s&Ntk=IMain&Ntx=mode+matchall'
    # FIXME:
    #https://www.clearancejobs.com/jobs
    #https://www.clearancejobs.com/jobs?RC=25&Ns=p_TimeStamp|1&Ntt=software&Ntk=IMain&Ntx=mode+matchall
    #https://www.clearancejobs.com/jobs?Ntx=mode+matchall&Ntk=IMain&RC=25&Ns=p_TimeStamp|1&Ntt=engineer
    #https://www.clearancejobs.com/jobs?Ntx=mode+matchall&Ntk=IMain&RC=25&Ns=p_TimeStamp|1&Ntt=python&No=25


    def parse_item(self,  response):
        item = super(ClearancejobsSpider, self).parse_item(response)
        item['description'] =  response.css('.cj-job-details').extract()[0] #div
        yield item


    def parse(self, response):
        super(ClearancejobsSpider,  self).parse(response)
        results = response.css('#search-results') # div
        rows = results.css('.cj-search-result-item')
        for row in rows:
            item = self.init_item(response)
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
