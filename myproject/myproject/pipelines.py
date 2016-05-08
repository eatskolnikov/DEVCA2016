# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exporters import JsonItemExporter
from scrapy import signals

class SanitizeItems(object):
    def process_item(self, item, spider):
        item['province'] =  item['province'].strip().lower()
        item['candidate'] =  ''.join(i for i in item['candidate'].strip() if i.isalpha() or i==' ').strip().lower()
        item['party'] =  item['party'].strip()
        item['position'] =  item['position'].strip().lower()
        return item

class SaveItemToJson(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_items.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file=file)
        print self.exporter
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item