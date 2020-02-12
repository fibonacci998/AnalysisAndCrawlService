# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from crawler.models import RealEstateObject, Quote
from pydispatch import dispatcher
from scrapy import signals

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, typeCrawl, *args, **kwargs):
        self.unique_id = unique_id
        self.typeCrawl = typeCrawl
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
            typeCrawl=crawler.settings.get('type')
        )

    def process_item(self, item, spider):
        if self.typeCrawl == 'reo':
            # print("price is "+str(item.get('price')[0])+", area is "+item.get('area')[0].rstrip().lstrip())
            reo = RealEstateObject(
                idPost = item.get('codePost')[0],
                typePost = item.get('typePost')[0],

                title = item.get('address')[0],
                price = item.get('price')[0],
                area = item.get('area')[0]
            )
            reo.idCrawlerJob = self.unique_id
            print('save new reo')
            reo.save()
        if self.typeCrawl == 'quote':
            quote = Quote(text=item.get('text'), author=item.get('author'))
            quote.unique_id = self.unique_id
            quote.save()
        # print(self.typeCrawl)
        # quote = Quote(text=item.get('text'), author=item.get('author'))
        # quote.unique_id = self.unique_id
        # quote.save()
        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
