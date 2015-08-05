# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import re
from datetime import datetime

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import datetime2datetimestr,  tablexpath2dict,  append


class ClearedconnectionsSpider(BaseSpider):
    name = "clearedconnections"
    allowed_domains = ["www.clearedconnections.com"]
    base_url = 'https://www.clearedconnections.com'
    # kdt1 to search with all words
    query_url = 'https://www.clearedconnections.com/JobSeekerX/SearchJobs.asp?kwrd=%(keyword)s&kwdt=1&btnSearch=Run+Search+Now'
    # FIXME: location is only usa and use state code or city
    # keywords are separated by +
    # https://www.clearedconnections.com/JobSeekerX/SearchJobs.asp?kwrd=software+engineer&kwdt=1&btnSearch=Run+Search+Now
    # next page
    # https://www.clearedconnections.com/JobSeekerX/SearchJobs.asp?kwrd=software+engineer&kwdt=1&btnSearch=Run+Search+Now&PG=2
    # advanced search
    #query_url = 'https://www.clearedconnections.com/JobSeekerX/SearchJobs.asp?SearchStartingPoint=MainSearchForm&txtaction=CREATE&ProfileID=&SubmitToSearch=Search&rvsd=-1&fromsearchpage=true&lcta=&st=%(location_state)s%2CAL&ckwr=&skll=&cg=&pstn=&slr1=0&slr2=0&bnus=&relo=&exp2=&lvl=&dgr=&trvl=&drss=&wrks=&bnft=&ln=&ctzn=&clrn=&visa=&lctr=&city=&st=%(location_state)s%2CAL&prvn=&zip=&cn=&zip1=&rdus=&cmsa=&pmsa=&msa=&reg=&udi1=&udi2=&udi3=&udi4=&udi5=&kwrd=%(keywords)s&kwdt=1&btnSearch=Run+Search+Now&JobSearchProfileName=%3CSaved+Search+Name%3E'
    

    def parse_item(self,  response):
        item = super(ClearedconnectionsSpider, self).parse_item(response)     
        try:
            item['description'] = response.xpath('//div[@class="viewjob"]').extract()[0]
        except IndexError:
            append(self.fail_url_path, 'failed to parse:' + response.url)
        else:
            table = response.xpath('//table[@class="LabelValueTable"]')
            details = tablexpath2dict(table)
            item['clearance'] = details.get('Security Clearances',  '')
        yield item


    def parse(self, response):
        super(ClearedconnectionsSpider,  self).parse(response)
        table = response.xpath('//table[@class="jstext"]')
        rows = table.xpath('.//tr')[3:]
        if len(rows) < 1:
            append(self.fail_url_path, 'no data:' + response.url)
            return
        for row in rows:
            item = self.init_item(response)
            cols = row.xpath('.//td')
            col_url = cols[1]
            onclick = col_url.xpath('.//a/@onclick').extract()[0]
            m = re.search("PopupViewWindow\('(.+?)'", onclick)
            if m:
                url = m.group(1)
            item['item_url'] = 'https://www.clearedconnections.com/JobSeekerX/' + url
            item['title'] = col_url.xpath('.//a/text()').extract()[0]
            col_published = cols[0]
            published = col_published.xpath('.//p/text()').extract()[0].strip()
            item['published'] = datetime2datetimestr(datetime.strptime(published,'%m/%d/%Y'))
            col_company = cols[3]
            try:
                item['company'] = col_company.xpath('.//a/text()').extract()[0].strip()
            except IndexError:
                item['company'] = col_company.xpath('.//p/text()').extract()[0].strip()
            col_loc = cols[2]
            loc = col_loc.xpath('./text()').extract()[0]
            try:
                item['locality'] ,  item['region'],  _ = loc.split('-')
            except ValueError:
                item['locality'] = loc
            # data not available in this website
            item['short_description'] = ''            
            item['salary'] = ''
            item['department'] = ''
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.pagination').xpath('.//a[contains(.,"Next")]/@href').extract()
        if next:
            self.logger.debug('next url: %s' % self.base_url + next[0])
            yield Request(
                self.base_url + next[0],  
                callback=self.parse, 
                meta={'keyword': response.meta['keyword'],  'location': response.meta['location']}
            )
        else:
            self.logger.debug('no next url')
