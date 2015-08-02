# https://stackoverflow.com/questions/21839676/how-to-write-a-downloadhandler-for-scrapy-that-makes-requests-through-socksipy
# https://gist.github.com/cydu/8a4b9855c5e21423c9c5
import random  
import logging

from txsocksx.http import SOCKS5Agent
from twisted.internet import reactor                                                                 

from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler, ScrapyAgent
from scrapy.xlib.tx import TCP4ClientEndpoint
from scrapy.core.downloader.webclient import _parse 
from scrapy.conf import settings
#Module `scrapy.conf` is deprecated, use `crawler.settings` attribute instead
# http://doc.scrapy.org/en/latest/topics/settings.html#how-to-access-settings


logger = logging.getLogger(__name__)


class Socks5DownloadHandler(HTTP11DownloadHandler):

    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        agent = ScrapySocks5Agent(contextFactory=self._contextFactory, pool=self._pool)
        logger.debug('Changing downloader agent...')
        logger.debug('response proxy: %s',  request.meta.get('proxy'))
        return agent.download_request(request)
        # no need for this, better not to use settings variable
#        if spider.settings.get('USE_SOCKS5PROXY',  False):
#        logger.debug('Not using Socks5Agent...')            
##        super(Socks5DownloadHandler, self).download_request(request, spider)
#        agent = ScrapyAgent(contextFactory=self._contextFactory, pool=self._pool,
#        maxsize=getattr(spider, 'download_maxsize', self._default_maxsize),
#        warnsize=getattr(spider, 'download_warnsize', self._default_warnsize))
#        return agent.download_request(request)
            
class ScrapySocks5Agent(ScrapyAgent):
        
    def _get_agent(self, request, timeout):
        bindAddress = request.meta.get('bindaddress') or self._bindAddress
        # this needs http_proxy environment variable or proxy middleware, 
        # otherwise it will be none
#        proxy = request.meta.get('proxy')
        proxy = settings.get('SOCKSPROXY',  '127.0.0.1:9050')
        logger.debug('downloader agent proxy: %s' % proxy)
        if proxy:
            _, _, proxyHost, proxyPort, proxyParams = _parse(proxy)
            _, _, host, port, proxyParams = _parse(request.url)
            proxyEndpoint = TCP4ClientEndpoint(reactor, proxyHost, proxyPort,
                                timeout=timeout, bindAddress=bindAddress)
            newcirc = settings.get('NEWCIRC',  False)
            if newcirc:
                username = hex(random.randint(0, 2**32))                            
                password = hex(random.randint(0, 2**32))
                agent = SOCKS5Agent(reactor, proxyEndpoint=proxyEndpoint,  endpointArgs=dict(methods=dict(login=(username,password))))
            else:
                agent = SOCKS5Agent(reactor, proxyEndpoint=proxyEndpoint)
            return agent
        return self._Agent(reactor, contextFactory=self._contextFactory,
            connectTimeout=timeout, bindAddress=bindAddress, pool=self._pool) 
            
# in settings:
#DOWNLOAD_HANDLERS = {
#'http': 'myspider.socks5_http.Socks5DownloadHandler',
#'https': 'myspider.socks5_http.Socks5DownloadHandler'
#} 
