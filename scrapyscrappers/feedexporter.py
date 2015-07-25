import json
import codecs

from scrapy.exporters import JsonLinesItemExporter,  JsonItemExporter

import logging

logger = logging.getLogger(__name__)

class UnicodeJsonLinesItemExporter(JsonLinesItemExporter):

    def __init__(self, file, **kwargs):
        filename = file.name
        file.close()
        file = codecs.open(filename, 'w', encoding='utf-8')
        kwargs['ensure_ascii'] = False
        super(UnicodeJsonLinesItemExporter, self).__init__(file, **kwargs)

    def _to_str_if_unicode(self, value):
        return value


class JsonIdentItemExporter(JsonItemExporter):
    """"
    JsonItemExporter with identation

    """

    def __init__(self, file, **kwargs):
        filename = file.name
        logger.debug(filename)
        kwargs['indent'] = 2
        # equivalent to
        #json.JSONEncoder(indent=4)
        super(JsonIdentItemExporter, self).__init__(file, **kwargs)
