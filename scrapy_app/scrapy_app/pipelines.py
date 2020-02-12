# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from crawler.models import RealEstateObject
from pydispatch import dispatcher
from scrapy import signals

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
        )

    def process_item(self, item, spider):
        reo = RealEstateObject(
            idPost = item.get('codePost')
            typePost = item.get('typePost')

            title = item.get('address')
            price = item.get('price')
            area = item.get('area')
        )
        reo.idCrawlerJob = reo.unique_id
        reo.save()
        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
