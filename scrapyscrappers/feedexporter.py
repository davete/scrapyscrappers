import json
import codecs

from scrapy.contrib.exporter import JsonLinesItemExporter

class UnicodeJsonLinesItemExporter(JsonLinesItemExporter):

    def __init__(self, file, **kwargs):
        filename = file.name
        file.close()
        file = codecs.open(filename, 'w', encoding='utf-8')
        kwargs['ensure_ascii'] = False
        super(UnicodeJsonLinesItemExporter, self).__init__(file, **kwargs)

    def _to_str_if_unicode(self, value):
        return value
