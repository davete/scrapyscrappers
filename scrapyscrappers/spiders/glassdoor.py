# -*- coding: utf-8 -*-
from scrapy.http import Request

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import timeago2datetimestr,  append


class GlassdoorSpider(BaseSpider):
    name = "glassdoor"
    # FIXME: check other domains 
    #allowed_domains = ["glassdoor.com"]
    base_url = 'http://glassdoor.com'
    query_url = 'http://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=%(keyword)s&sc.keyword=%(keyword)s&locT=&locId=&jobType=all'
    # with several keywords, keywords are separated by +
    # http://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=python+ruby&sc.keyword=python+ruby&locT=C&locId=1147401&jobType=all
    # FIXME: location,location use self state code and self id


    def parse_item(self,  response):
        item = super(GlassdoorSpider, self).parse_item(response)
        # items are in different domains, store al page
        if not response.url.startswith(self.base_url):
            item['description'] = response.body
        yield item


    def parse(self, response):
        super(GlassdoorSpider,  self).parse(response)
#        list = response.css('.standardJobListings')
        list = response.css('.jlGrid')
        rows = list.xpath('.//div[@itemtype="http://schema.org/JobPosting"]')
        if len(rows) < 1:
            append(self.fail_url_path, 'no data:' + response.url)
            return
        for row in rows:
            item = self.init_item(response)
            url = row.xpath('.//h3[@itemprop="title"]/a/@href').extract()[0]
            item['item_url'] = self.base_url + url
            # a text could have span tag inside
            item['title'] = row.xpath('string(.//h3[@itemprop="title"]/a)').extract()[0].strip()
            item['company'] = row.xpath('string(.//span[@class="employerName"])').extract()[0].strip()
            published = row.css('.logo').css('.minor::text').extract()[0].strip()
            item['published'] =  timeago2datetimestr(item['date_search'],  published)
            item['short_description'] = row.xpath('string(.//p[@itemprop="description"])').extract()[0].strip()
            loc = row.xpath('string(.//span[@itemprop="addressLocality"])').extract()[0].strip()
            try:
                item['locality'] ,  item['region']  = loc.split(', ')
            except ValueError:
                item['locality'] = loc
                item['region'] = ''
            # data not available in this website
            item['salary'] = ''
            item['clearance'] = ''
            item['department'] = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.next a::attr(href)').extract()
        if next:
            self.logger.debug('next url: %s' % self.base_url + next[0])
            yield Request(
                # self.base_url + next[0]['href'],  # with soup
                self.base_url + next[0], 
                callback=self.parse, 
                meta={'keyword': response.meta['keyword'],  'location': response.meta['location']}
            )
        else:
            self.logger.debug('no next url')
