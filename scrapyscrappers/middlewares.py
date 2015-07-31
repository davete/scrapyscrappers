import os
import random
import logging
import json

from scrapy import signals
from scrapy.conf import settings
#Module `scrapy.conf` is deprecated, use `crawler.settings` attribute instead
# http://doc.scrapy.org/en/latest/topics/settings.html#how-to-access-settings

from .agents import AGENTS

logger = logging.getLogger(__name__)

# https://pkmishra.github.io/blog/2013/03/18/how-to-run-scrapy-with-TOR-and-multiple-browser-agents-part-1-mac/
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        #ua  = random.choice(settings.get('USER_AGENT_LIST'))
        ua = random.choice(AGENTS)
        if ua:
            logger.debug('Changing ua %s' % ua)
            request.headers.setdefault('User-Agent', ua)
            #request.headers['User-Agent'] = agent
        
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
        logger.debug('using proxy %s' % request.meta['proxy'] ) 

#https://github.com/ikeikeikeike/scrapy-proxies
class BaseHttpProxyMiddleware(object):

    def __init__(self, http_proxy):
        self._http_proxy = http_proxy

    def spider_opened(self, spider):
        """ signal receiver
        """
        self._http_proxy = getattr(spider, 'http_proxy', self._http_proxy)

    def process_request(self, request, spider):
        """ pre request
        """
        if self.use_proxy(request):
            try:
                request.meta['proxy'] = self._http_proxy
            except Exception, e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        # if "depth" in request.meta and int(request.meta['depth']) <= 2:
            # return False
        # i = random.randint(1, 10)
        # return i <= 2
        #return True
        return settings.get('USE_PROXY',  False)


class FAHttpProxyMiddleware(BaseHttpProxyMiddleware):
    """ Factory Automation http proxy provider.
    """
    @classmethod
    def from_crawler(cls, crawler):
        """ signal multiple spiders.
        """
        proxies_path = crawler.settings.get('PROXIES_PATH')
        logger.debug('proxies path: %s' % proxies_path)
        with open(proxies_path) as f:
            proxies = json.load(f)
        proxy = random.choice(proxies)
        logger.debug('proxy %s' % proxy)
        klass = cls(proxy)
        crawler.signals.connect(klass.spider_opened, signal=signals.spider_opened)
        return klass


class HttpProxyMiddleware(BaseHttpProxyMiddleware):
    """ fixed http proxy provider.
    """
    @classmethod
    def from_crawler(cls, crawler):
        """ signal multiple spiders.
        """
        http_proxy = crawler.settings.get('HTTP_PROXY', 'http://127.0.0.1:8123')
        klass = cls(http_proxy)
        crawler.signals.connect(klass.spider_opened, signal=signals.spider_opened)
        return klass
        
