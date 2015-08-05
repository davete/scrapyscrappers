# -*- coding: utf-8 -*-
from scrapy.http import Request

from datetime import datetime

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import datetime2datetimestr,  append


class ClearedjobsSpider(BaseSpider):
    name = "clearedjobs"
    allowed_domains = ["clearedjobs.net"]
    base_url = 'http://clearedjobs.net'
    query_url = 'http://clearedjobs.net/index.php?action=advanced_search&page=search&zip_radius=20&keywords=%(keyword)s&city_state_zip=%(location)s&security_clearance=&submit=SEARCH+JOBS'
    # keywords are separated by +
    # next url
    # http://clearedjobs.net/search/action/advanced_search/zip_radius/20/keywords/software/city_state_zip/+/security_clearance/+/submit/SEARCH+JOBS/start/25


    def parse_item(self,  response):
        item = super(ClearedjobsSpider, self).parse_item(response)
        try:
            item['description'] = response.css('.view_long').extract()[0]
            item['salary'] = response.css('.view_job').xpath('.//div//div[contains(.,"Salary:")]/following-sibling::div[1]/text()').extract()[0].strip()
        except IndexError:
            append(self.fail_url_path, 'failed to parse:' + response.url)
        yield item


    def parse(self, response):
        super(ClearedjobsSpider,  self).parse(response)
        table = response.xpath('//table[@class="search_res"]//tbody')
        rows = table.xpath('.//tr')
        if len(rows) < 1:
            append(self.fail_url_path, 'no data:' + response.url)
            return
        for row in rows:
            item = self.init_item(response)
            cols = row.xpath('.//td')
            col0 = cols[0]
            url = col0.xpath('.//a[@class="search"]/@href').extract()[0]
            item['item_url'] = self.base_url + "/" + url
            # a text could have span tag inside
            item['title'] = col0.xpath('string(.//a[@class="search"])').extract()[0].strip()
            item['company'] = col0.xpath('.//div[@class="info"]//a/text()').extract()[0]
            try:
                item['clearance'] = col0.xpath('.//div[@class="desc"]/text()').extract()[0]
            except IndexError:
                # item['clearance'] = ''
                pass
            published = col0.xpath('.//div[@class=""]/text()').extract()[0].replace('Posted - ','')
            item['published'] = datetime2datetimestr(datetime.strptime(u'July 8, 2015', '%B %d, %Y'))
            col1 = cols[1]
            loc = col1.xpath('./text()').extract()[0].strip()
            try:
                item['locality'] ,  item['region']  = loc.split(', ')
            except ValueError:
                item['locality'] = loc
                item['region'] = ''
            # data not available in this website
            item['short_description'] = ''
            item['department'] = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.navbar_bottom').xpath('.//a[text()=">"]/@href').extract()
        if next:
            if next[0].startswith('/'):
                self.logger.debug('next url: %s' % self.base_url +next[0])
                yield Request(
                    self.base_url + next[0],  
                    callback=self.parse, 
                    meta={'keyword': response.meta['keyword'],  'location': response.meta['location']}
                )
            else:
                self.logger.debug('next url: %s' % self.base_url + '/'  +next[0])
                yield Request(
                    self.base_url + '/' + next[0],  
                    callback=self.parse, 
                    meta={'keyword': response.meta['keyword'],  'location': response.meta['location']}
                )
        else:
            self.logger.debug('no next url')
