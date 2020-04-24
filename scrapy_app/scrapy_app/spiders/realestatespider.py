# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
import json
from string import Template
class RealEstateSpider(CrawlSpider):
    name = 'realestatespider'
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
        for linkEachItem in response.css(self.config['reoconfig']['cssselector']['allpost']).extract():  
            yield scrapy.Request("https://" + self.domain+"/"+linkEachItem, callback=self.crawlDataRealEstate)

    def convertPriceToNumber(self, price, area):
        priceConverted = price
        if (len(price[0].split()) > 0):
            if (price[0].split()[1] == u'tỷ'):
                priceConverted = float(price[0].split()[0]) * 1000000000
            elif (price[0].split()[1] == u'triệu'):
                priceConverted = float(price[0].split()[0]) * 1000000
            elif (price[0].split()[1] == u'triệu/m²' and type(area) == float and area != -1):
                priceConverted = float(price[0].split()[0]) * 1000000 * area
            else:
                priceConverted = -1
        return priceConverted

    def getValue(self, response, css, wantFullText=False, position=0, isNumber = False):
        valueExtract = response.css(css).extract()
        if (len(valueExtract) > 0):
            if (wantFullText):
                return valueExtract[position].rstrip().lstrip()
            else:
                return valueExtract[position].split()[0].rstrip().lstrip()
        if (isNumber): return "-1"
        return None

    def crawlDataRealEstate(self, response):
       
        configPost = self.config['reoconfig']['cssselector']
        
        codePost = self.getValue(response, configPost['codePost'])
        
        type = self.getValue(response, configPost['type'], True)

        address = self.getValue(response, configPost['address'], True)

        numberBedrooms = self.getValue(response, configPost['numberBedrooms'], isNumber=True)

        numberToilets = self.getValue(response, configPost['numberToilets'], isNumber=True)

        area = self.getValue(response, configPost['area']['value'], isNumber=True)
        if (configPost['area']['split-m2'] == "true"):
            try:
                area = float(area.split('m')[0].replace(',','.'))
            except:
                area = -1
 

        price = response.css(configPost['price']['value']).extract()
        if (configPost['price']['split-price'] == "true"):
            price = self.convertPriceToNumber(price, area)
        
        
        longitude = self.getValue(response, configPost['longitude'], isNumber=True)
        if (longitude != None): longitude = float(longitude)
        latitude = self.getValue(response, configPost['latitude'], isNumber=True)
        if (latitude != None): latitude = float(latitude)
        nameOwner = self.getValue(response, configPost['nameOwner'],True)
        mobile = self.getValue(response, configPost['mobile'], True)
        email = self.getValue(response, configPost['email'], True)
        sizeFront = self.getValue(response, configPost['sizeFront'], isNumber=True)
        if (sizeFront != None): sizeFront = float((sizeFront).replace(',','.'))
        numberFloor = self.getValue(response, configPost['numberFloor'], isNumber=True)
        if (numberFloor != None): numberFloor = float((numberFloor).replace(',','.'))
        wardin = self.getValue(response, configPost['wardin'])
        if (wardin != None): wardin = float((wardin).replace(',','.'))
        homeDirection = self.getValue(response, configPost['homeDirection'], True)
        balconyDirection = self.getValue(response, configPost['balconyDirection'], True)
        interior = self.getValue(response, configPost['interior'], True)
        projectSize = self.getValue(response, configPost['projectSize'], True)
        projectName = self.getValue(response, configPost['projectName'], True)
        projectOwner = self.getValue(response, configPost['projectOwner'], True)
        
        dateTemp = self.getValue(response, configPost['startDatePost'],True, -1)
        startDatePost = datetime.strptime(dateTemp,'%d-%m-%Y').date()
        dateTemp = self.getValue(response, configPost['endDatePost'],True, -1)
        endDatePost = datetime.strptime(dateTemp,'%d-%m-%Y').date()
        typePost = self.getValue(response, configPost['typePost'], True, -1)


        item={}
        item['type'] = type
        item['address'] = address
        item['numberBedrooms'] = numberBedrooms
        item['numberToilets'] = numberToilets
        item['nameOwner'] = nameOwner
        item['mobile'] = mobile
        item['email'] = email
        item['price'] = price
        item['area'] = area
        item['longitude'] = longitude
        item['latitude'] = latitude
        item['link'] = response.request.url
        item['sizeFront'] = sizeFront
        item['numberFloor'] = numberFloor
        item['wardin'] = wardin
        item['homeDirection'] = homeDirection
        item['balconyDirection'] = balconyDirection
        item['interior'] = interior
        item['projectName'] = projectName
        item['projectSize'] = projectSize
        item['projectOwner'] = projectOwner
        item['codePost'] = codePost
        item['startDatePost'] = startDatePost
        item['endDatePost'] = endDatePost
        item['typePost'] = typePost
        item['domain'] = self.domain
        yield item
