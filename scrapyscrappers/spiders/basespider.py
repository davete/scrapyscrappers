# -*- coding: utf-8 -*-
from datetime import datetime
from os.path import join

from scrapy import Spider
from scrapy.http import Request
#from scrapy.conf import settings
#from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from scrapyscrappers.items import ScrapyscrappersItem
from scrapyscrappers.util import obtain_keywords,  obtain_locations,  \
    current_datetime, now_timestamp,  save_html,  string2filename,  \
    url2filename ,  append


settings = get_project_settings()


class BaseSpider(Spider):
    handle_httpstatus_list = [403,  404,  503,  502]
    fail_url_path = settings.get('LOG_FAIL_URL_FULLPATH')

    def check_ip(self, response):
        sel = response.xpath('//body/text()')
        sel_ip.re('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')[0]
        self.logger.info("Public IP is: " + ip)


    def handle_response(self,  response):
        self.logger.debug('in handle response')
        try:
            if response.status == 200:
                append(settings.get('LOG_OK_URL_FULLPATH'), response.url)
            else:
                self.logger.debug('error http code: %s',  response.status)
                append(settings.get('LOG_FAIL_URL_FULLPATH'), str(response.status) + ': ' + response.url)
        except Exception, e:
            self.logger.exception(e)


    def __init__(self, keywords="", locations="",  *args, **kwargs):
        self.logger.debug('in init')
#        super(BaseSpider, self).__init__(*args, **kwargs)
        #FIXME: add the possibility to have a keyword that is several words
        if keywords:
            self.keywords = keywords.split(',')
        else: 
            self.keywords = obtain_keywords()
        self.logger.debug('keywords:')
        self.logger.debug(self.keywords)
        if locations:
            self.locations = locations.split(',')
        else:
            self.locations = obtain_locations()
        
        # TODO
        #to change proxy per spider
#        import json
#        with open(settings.get('PROXIES_PATH')) as f:
#            proxies = json.loads(f)
#        self.proxy_pool = proxies


    def start_requests(self):
        self.logger.debug('in start requests')
        # TODO: in the case of using http proxy, to check the public ip
#        yield Request('http://checkip.dyndns.org/', callback=self.check_ip)
        for location in self.locations:
            for keyword in self.keywords:
                url_params = {'keyword': keyword,  'location': location}
                url = self.query_url % url_params
                self.logger.debug('request url %s' % url)
#                yield Request(url, meta={'keyword': keyword,  'location': location})
                yield Request(url, meta=url_params)

#    def get_request(self, url):
#        req = Request(url=url)
#        if self.proxy_pool:
#            proxy_addr = self.proxy_pool[random.randint(0,len(self.proxy_pool) - 1)]
#            req.meta['proxy'] = proxy_addr
#        return req


    def parse_item(self,  response):
        self.logger.debug('parse_item %s' % response.url)
        item = response.meta['item']      
        args = {
        'name': self.name,  
        'location': item['location_search'],  
        'keyword': item['keyword'], 
#        'item': string2filename(item['title']), 
        'item': url2filename(item['item_url']), 
        'time': now_timestamp()
        }
        save_html(response.body,  args)
        return item


    def init_item(self,  response):
        item = ScrapyscrappersItem()
        item['keyword'] = response.meta['keyword']
        item['location_search'] = response.meta['location']
        item['date_search'] = current_datetime()
        return item


    def parse(self, response):
        self.logger.debug('parsing %s' % response.url)
        self.handle_response(response)
        args = {
        'name': self.name,  
        'location': response.meta['location'],  
        'keyword': response.meta['keyword'], 
#        'item': 'list', 
        'item': url2filename(response.url), 
        'time': now_timestamp()
        }
        save_html(response.body,  args)
