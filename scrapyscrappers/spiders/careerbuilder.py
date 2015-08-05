# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.conf import settings

from scrapyscrappers.spiders.basespider import BaseSpider
from scrapyscrappers.util import timeago2datetimestr,  append


class CareerbuilderSpider(BaseSpider):
    name = "careerbuilder"
    allowed_domains = ["www.careerbuilder.com"]
    base_url = 'https://www.careerbuilder.com'
    query_url = 'https://www.careerbuilder.com/jobseeker/jobs/jobresults.aspx?s_rawwords=%(keyword)s&s_freeloc=%(location)s'
    # several keywords separated by +
    # https://www.careerbuilder.com/jobseeker/jobs/jobresults.aspx?s_rawwords=python+django&s_freeloc=
    # next url
    # http://www.careerbuilder.com/jobseeker/jobs/jobresults.aspx?excrit=st%3da%3buse%3dALL%3brawWords%3dpython+django%3bCID%3dUS%3bSID%3d%3f%3bTID%3d0%3bLOCCID%3dUS%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bPDQ%3dAll%3bPAYL%3d0%3bPAYH%3dgt120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bCHL%3dAL%3bQS%3dsid_unknown%3bSS%3dNO%3bTITL%3d0%3bOB%3d-relv%3bJQT%3dRAD%3bJDV%3dFalse%3bSITEENT%3dUSJob%3bMaxLowExp%3d-1%3bRecsPerPage%3d25&pg=2&IPath=JRKV

    def parse_item(self,  response):
        item = super(CareerbuilderSpider,  self).parse_item(response)
        #soup = bs4.BeautifulSoup(response.body)     
        #item['title'] = response.xpath('//h1/span/text()').extract()
        #if DEBUG == False:
        #item['description'] = response.css('article').extract()[0]
        # or
        # or to dont get html tags
        #item['description'] = bs4.BeautifulSoup(response.body).select('article')[0].text
        try:
            item['description'] = response.xpath('//article').extract()[0]
        except IndexError:
            append(self.fail_url_path, 'failed to parse:' + response.url)
        # attribute not provided
        # item['clearance'] = ''
        yield item


    def parse(self, response):
        super(CareerbuilderSpider,  self).parse(response)
        rows = response.css('.gs-job-result-abstract')
        if len(rows) < 1:
            append(self.fail_url_path, 'no data:' + response.url)
            return
        for row in rows:
            item = self.init_item(response)
            item['item_url'] = row.css('.jt').xpath('@href').extract()[0]
            item['title'] = row.css('.jt::text').extract()[0]
            #item['short_description'] = row.css('span[itemprop="description"]::text').extract()[0]
            # the same with xpath
            item['short_description'] = row.xpath('.//span[@itemprop="description"]/text()').extract()[0]
            item['company'] = row.xpath('.//a/@companyname').extract()[0]
            # or
#            try:
#                item['company'] = row.xpath('.//td[@itemprop="hiringOrganization"]/a/text()').extract()[0]
#            except IndexError:
#                self.logger.debug(row.xpath('.//td[@itemprop="hiringOrganization"]/a/text()').extract())
            location = row.xpath('.//div[@itemprop="jobLocation"]/span/text()').extract()[0]
            try:
                item['region'] ,  item['locality'] = location.split(' - ')
            except ValueError:
                item['locality'] = location
            teaser = [i.strip() for i in row.xpath('.//div[contains(@id, "pnlTeaser")]/p/text()').extract()[0].split('|')]
            if len(teaser) == 2:
                item['salary'] = teaser[1].split(':')[1]
            else:
                item['salary'] = ''
            item['department'] = ''
            ago = row.css('.jl_rslt_posted_cell span::text').extract()[0]
            item['published'] = timeago2datetimestr(item['date_search'] , ago)
            self.logger.debug('title %s' % item['title'])
            yield Request(item['item_url'],  callback=self.parse_item, meta={'item': item} )
        next = response.css('.JL_MXDLPagination2_next').xpath('@href').extract()
        if next:
            self.logger.debug('next url: %s' % next[0])
            yield Request(
                next[0], 
                callback=self.parse, 
                meta={'keyword': response.meta['keyword'],  'location': response.meta['location']}
            )
        else:
            self.logger.debug('no next url')
