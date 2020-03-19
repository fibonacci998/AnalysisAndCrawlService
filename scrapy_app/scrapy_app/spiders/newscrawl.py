# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
import json
from string import Template
class NewsCrawlSpider(CrawlSpider):
    name = 'newscrawl'
    page_number = 1

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.settingXpath = kwargs.get('xpath')
        self.start_urls = [self.url]
        self.url = self.start_urls[0]
        temp = kwargs.get('config')
        self.config = json.loads(temp)
        page_number = 1
    def start_request(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):

        for i in range(self.config['pageconfig']['numberpage']):
            
            template = Template(self.config['pageconfig']['pageurltemplate'])
            urlPage = template.substitute(page=str(self.page_number))
            self.page_number += 1
            yield scrapy.Request(urlPage, callback=self.crawlDataTotalPage)
            
    def crawlDataTotalPage(self, response):
        configCss = self.config['newsconfig']['cssselector']
        print("config here: "+configCss['allpost'])
        allDiv = response.css(configCss['allpost'])
        for news in allDiv:
            link = news.css(configCss['link']).extract()
            imageLink = news.css(configCss['imagelink']).extract()[0]
            title = news.css(configCss['title']).extract()[0]
            description = ''.join(news.css(configCss['description']).extract()).lstrip().rstrip()
            yield{
                'link' : 'https://'+self.domain+link[0],
                'imageLink' : imageLink,
                'title' : title,
                'description' : description,
                'domain' : self.domain
            }
