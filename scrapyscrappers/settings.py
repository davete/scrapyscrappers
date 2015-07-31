# -*- coding: utf-8 -*-

# Scrapy settings for scrapyscrappers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


from os.path import dirname,  join,  abspath
#from scrapy.extensions.httpcache import DummyPolicy

BOT_NAME = 'scrapyscrappers'

SPIDER_MODULES = ['scrapyscrappers.spiders']
NEWSPIDER_MODULE = 'scrapyscrappers.spiders'


# FIXME: change in producion
DEBUG=True
JSON_DIR = 'json'
DATA_DIR = 'data'
LOG_DIR = 'log'
LOG_FILENAME =  BOT_NAME + '.log'
BASE_PATH = dirname(dirname(abspath(__file__)))
JSON_PATH = join(BASE_PATH,  JSON_DIR)
DATA_PATH = join(BASE_PATH,  DATA_DIR)
LOG_PATH = join(BASE_PATH,  LOG_DIR)
LOG_FULLPATH = join(LOG_PATH,  LOG_FILENAME)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyscrappers (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False
COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapyscrappers.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapyscrappers.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# with no default HttpProxyMiddleware, the environment variables will be used
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware':500, 
    'scrapyscrappers.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#    'scrapyscrappers.middlewares.ProxyMiddleware': 410,
    # to rotate proxies
    'scrapyscrappers.middlewares.FAHttpProxyMiddleware': 410, 
    # no need to disable default proxymiddleware
#    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':  None, 
    # the priority to change the proxy should be higher than the retry, in case the proxy doesn't only change on retry
#    'scrapyscrappers.middlewares_retry.RetryChangeProxyMiddleware': 200,
#    'scrapyscrappers.middlewares_retry.RetryChangeCircuit': 200,    
#    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapyscrappers.pipelines.SomePipeline': 300,
#}

#ITEM_PIPELINES = {
#    'scrapyscrappers.pipelines.ScrapyscrappersPipeline': 300, 
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

#HTTPCACHE_ENABLED = True # default False
HTTPCACHE_DIR = DATA_PATH # default 'httpcache'
#HTTPCACHE_EXPIRATION_SECS = 0 # Set to 0 to never expire, default 0
#HTTPCACHE_GZIP = False # default False
#HTTPCACHE_POLICY = DummyPolicy # default DummyPolicy

## extra settings

# FIXME: change in producion
LOG_LEVEL = 'DEBUG'
#LOG_LEVEL = 'INFO'

#LOG_ENABLED = True
# uncomment to log to file
#LOG_FILE = LOG_FULLPATH
#LOG_ENCODING = 'utf-8'
#STATS_DUMP = True # default True

COMPRESSION_ENABLED = False # default True
#DOWNLOAD_DELAY = 2 # default 0
#RANDOMIZE_DOWNLOAD_DELAY = True # default True


HTTP_PROXY = 'http://127.0.0.1:8118'

#DOWNLOAD_HANDLERS = {
#    # comment this to don't use socks proxy
#    'http': 'scrapyscrappers.downloaders.Socks5DownloadHandler',
#    'https': 'scrapyscrappers.downloaders.Socks5DownloadHandler'
#} 

#FEED_FORMAT = "jsonlines"
FEED_FORMAT = "jsonident"
FEED_URI = "file:///" + join(JSON_PATH, "%(name)s-%(time)s.json")
#FEED_URI = "file:///" + join(JSON_PATH, "%(keyword)s-%(name)s-%(time)s.json")

# FIXME: instead of creating a new exporter, see how to pass the encoder 
#json.JSONEncoder(indent=4)
FEED_EXPORTERS = {
 'jsonident': 'scrapyscrappers.feedexporter.JsonIdentItemExporter'
}

## custom variables

KEYWORDS_FILE = 'keywords.txt'
LOCATIONS_FILE = 'locations.txt'
KEYWORDS_PATH = join(BASE_PATH,  KEYWORDS_FILE)
LOCATIONS_PATH = join(BASE_PATH,  LOCATIONS_FILE)
DATETIME_FORMAT = '%Y-%m-%d %H:%M'
HTML_DIR = 'html'
HTML_PATH= join(HTML_DIR, "%(name)s-%(location)s-%(keyword)s-%(item)s-%(time)s.html")
LOG_OK_URL_FILENAME = 'ok_url.log'
LOG_FAIL_URL_FILENAME = 'fail_url.log'
LOG_OK_URL_FULLPATH = join(LOG_PATH,  LOG_OK_URL_FILENAME)
LOG_FAIL_URL_FULLPATH = join(LOG_PATH,  LOG_FAIL_URL_FILENAME)


# For socks proxy
SOCKSPROXY = 'http://127.0.0.1:9050'
NEWCIRC = True

# For HttpProxyMiddleware
USE_PROXY = True
PROXIES_FILE = 'proxies.json'
PROXIES_PATH = join(DATA_PATH,  PROXIES_FILE)


try:
    from settings_local import *
except:
    pass
