# -*- coding: utf-8 -*-
from datetime import datetime,  timedelta
from os.path import exists
from settings import KEYWORDS_PATH,  LOCATIONS_PATH,  DATETIME_FORMAT,  HTML_PATH
from scrapy.conf import settings
import logging

logger = logging.getLogger(__name__)

def obtain_keywords():
    if exists(KEYWORDS_PATH):
        with open(KEYWORDS_PATH) as f:
            keywordsstr = f.read()
        return keywordsstr.split()
    return ['']

def obtain_locations():
    if exists(LOCATIONS_PATH):
        with open(LOCATIONS_PATH) as f:
            locationsstr = f.read()
        return locationsstr.split()
    return ['']

def current_datetime():
    return datetime.now().strftime(DATETIME_FORMAT)

def now_timestamp():
    return datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')

def datetimestr2datetime(datetimestr):
    return datetime.strptime(datetimestr, DATETIME_FORMAT)

def datetime2datetimestr(dt):
    return dt.strftime(DATETIME_FORMAT)

def timeago2datetimestr(datetimestr,  timeago):
    # timeago is an sting like: 
    # +30 days ago, 30+ days ago, 1 day ago, 18 hours ago
    timeagolist = timeago.split()
    if timeagolist[1] == 'days' or 'day':
        # + could be on the left or right of the number
        td = timedelta(days=int(timeagolist[0].replace('+',  '')))
    if timeagolist[1] == 'hours':
        td = timedelta(hours=int(timeagolist[0]))
    delta = datetimestr2datetime(datetimestr)  - td
    return datetime2datetimestr(delta)

# for usajobs
def table2dict(soup,  htmltag):
    details = {}
    tables  = soup.select(htmltag)
    logger.debug('tables %s' % len(tables))
    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td', limit=2)
            try:
                details[cells[0].stripped_strings.next().replace(':','')] = cells[1].stripped_strings.next()
            except IndexError:
                # less than 2 columns
                pass
    return details

# for clearedconnections
def tablexpath2dict(table):
    details = {}
    rows = table.xpath('.//tr')
    for row in rows:
        try:
            details[row.xpath('./th/text()').extract()[0].replace(':', '')] = row.xpath('./td/text()').extract()[0]
        except:
            pass
    return details


# for usajobs, not being used
def divjobinfo12dict(soup):
    details = {}
    div  = soup.select('div#jobinfo1')[0]
    for p in div.find_all('p'):
        key = p.select('strong')[0].text.strip().replace(':','')
        value = p.select('span.info')[0].stripped_strings.next()
        details[key] = value
    return details

def html2str(html):
#    import lxml.html
#    import lxml.etree
#    root = lxml.html.fromstring(desc)
#    return lxml.html.tostring(root, method="text", encoding=unicode)
    return bs4.BeautifulSoup(html).text


def save_html(body,  args):
    html_path = settings.get('HTML_PATH') % args
    with open(html_path,  'w') as f:
        f.write(body)
    logger.debug('saving html %s' % html_path)


def string2filename(text):
    return "".join(x for x in text.lower() if x.isalnum())
    

def url2filename(text):
    return text.replace(' ', '_').replace('https://', '').replace('http://','').replace('/', '_')


def append(file, string):
    file = open(file, 'a')
    file.write(string+"\n")
    file.close()
