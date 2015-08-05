#! /usr/bin/env python

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#from scrapyscrappers.spiders.simplyhired import SimplyhiredSpider
#from scrapyscrappers.spiders.usajobs import UsajobsSpider


process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('simplyhired')
process.crawl('usajobs')
process.crawl('careerbuilder')
process.crawl('glassdoor')
process.crawl('clearedjobs')
process.crawl('clearedconnections')
process.crawl('clearancejobs')
process.start() # the script will block here until the crawling is finished
