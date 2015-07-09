from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from scrapyscrappers.spiders.simplyhired import SimplyhiredSpider
from scrapyscrappers.spiders.usajobs import UsajobsSpider

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(SimplyhiredSpider)
d = runner.crawl(UsajobsSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished

# FIXME: see how to run the scrappers being able to stop and resume
