# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from crawler.models import RealEstateObject, News
from pydispatch import dispatcher
from scrapy import signals
from crawler.serializers import GetAllRealEstateObjectSerializer, GetAllNewsSerializer
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
            reo = RealEstateObject(
                codePost = item.get('codePost'),
                typePost = item.get('typePost'),

                title = item.get('address'),
                price = item.get('price'),
                area = item.get('area'),

                type = item.get('type'),
                address = item.get('address'),
                numberBedrooms = item.get('numberBedrooms'),
                numberToilets = item.get('numberToilets'),
                nameOwner = item.get('nameOwner'),
                mobile = item.get('mobile'),
                email = item.get('email'),
                longitude = item.get('longitude'),
                latitude = item.get('latitude'),
                link = item.get('link'),
                sizeFront = item.get('sizeFront'),
                numberFloor = item.get('numberFloor'),
                wardin = item.get('wardin'),
                homeDirection = item.get('homeDirection'),
                balconyDirection = item.get('balconyDirection'),
                interior = item.get('interior'),
                projectName = item.get('projectName'),
                projectSize = item.get('projectSize'),
                projectOwner = item.get('projectOwner'),
                startDatePost = item.get('startDatePost'),
                endDatePost = item.get('endDatePost')
            )
            reo.idCrawlerJob = self.unique_id
            search = RealEstateObject.objects.filter(link=reo.link)
            data = GetAllRealEstateObjectSerializer(search, many = True)
            if (len(data.data)==0):
                reo.save()
        elif self.typeCrawl == 'news':
            news = News(
                link = item.get('link'),
                imageLink = item.get('imageLink'),
                title = item.get('title'),
                description = item.get('description')
            )
            news.idCrawlerJob = self.unique_id
            search = News.objects.filter(link=news.link)
            data = GetAllNewsSerializer(search, many = True)
            if (len(data.data)==0):
                news.save()
         
        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
