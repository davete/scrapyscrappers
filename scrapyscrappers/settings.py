# -*- coding: utf-8 -*-

# Scrapy settings for scrapyscrappers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from os.path import dirname,  join,  abspath

BOT_NAME = 'scrapyscrappers'

SPIDER_MODULES = ['scrapyscrappers.spiders']
NEWSPIDER_MODULE = 'scrapyscrappers.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'
# FIXME: change in producion
#LOG_LEVEL = 'DEBUG'
LOG_LEVEL = 'INFO'

#DEBUG=True
JSON_DIR = 'json'
DATA_DIR = 'data'
KEYWORDS_FILE = 'keywords.txt'
LOCATIONS_FILE = 'locations.txt'
BASE_PATH = dirname(dirname(abspath(__file__)))
JSON_PATH = join(BASE_PATH,  JSON_DIR)
DATA_PATH = join(BASE_PATH,  DATA_DIR)
KEYWORDS_PATH = join(BASE_PATH,  KEYWORDS_FILE)
LOCATIONS_PATH = join(BASE_PATH,  LOCATIONS_FILE)
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0 # Set to 0 to never expire
HTTPCACHE_DIR = DATA_PATH

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 300,
}

#FEED_FORMAT = "jsonlines"
FEED_FORMAT = "jsonident"
FEED_URI = "file:///" + join(JSON_PATH, "%(name)s-%(time)s.json")
#FEED_URI = "file:///" + join(JSON_PATH, "%(keyword)s-%(name)s-%(time)s.json")

# FIXME: instead of creating a new exporter, see how to pass the encoder 
#json.JSONEncoder(indent=4)
FEED_EXPORTERS = {
 #'jsonlines': 'scrapy.contrib.exporter.JsonLinesItemExporter', 
 'jsonident': 'scrapyscrappers.feedexporter.JsonIdentItemExporter'
}

