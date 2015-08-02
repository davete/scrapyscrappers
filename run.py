#! /usr/bin/env python

from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.conf import settings

from scrapyscrappers.spiders.simplyhired import SimplyhiredSpider
from scrapyscrappers.spiders.usajobs import UsajobsSpider
from scrapyscrappers.spiders.careerbuilder import CareerbuilderSpider
from scrapyscrappers.spiders.clearedconnections import ClearedconnectionsSpider
from scrapyscrappers.spiders.clearedjobs import ClearedjobsSpider
from scrapyscrappers.spiders.glassdoor import GlassdoorSpider
from scrapyscrappers.spiders.clearancejobs import ClearancejobsSpider


configure_logging({'LOG_FORMAT': settings.get('LOG_FORMAT')})
runner = CrawlerRunner()

d = runner.crawl(SimplyhiredSpider)
d = runner.crawl(UsajobsSpider)
d = runner.crawl(CareerbuilderSpider)
d = runner.crawl(ClearedconnectionsSpider)
d = runner.crawl(ClearedjobsSpider)
d = runner.crawl(GlassdoorSpider)
d = runner.crawl(ClearancejobsSpider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished

# FIXME: see how to run the scrappers being able to stop and resume
