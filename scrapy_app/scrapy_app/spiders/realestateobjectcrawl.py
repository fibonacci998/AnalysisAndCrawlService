# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class RealestateobjectcrawlSpider(CrawlSpider):
    name = 'realestateobjectcrawl'
    start_urls = ['https://batdongsan.com.vn/nha-dat-ban-ha-noi']

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.settingXpath = kwargs.get('xpath')
        
        self.start_urls = [self.url]
        self.url = self.start_urls[0]
        print("domain:" + self.domain)
        print("url: "+self.url)
        # self.allowed_domains = [self.domain]

    def start_request(self):
        print("start request")
        print("url here:" + self.url)
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        print("start parse")
        print("url here:"+response.url)
        yield scrapy.Request(response.url, callback=self.crawlDataTotalPage)
        # next_page_url = response.css(self.settingXpath['next_page_url']).extract()
        # if (next_page_url is not None):
        #     yield scrapy.Request(response.urljoin(next_page_url))

        # return super().parse(response)

    def crawlDataTotalPage(self, response):
        print("start parse item")
        # one item is a post about real estate object
        print(response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "p-title", " " ))]//a/@href').extract())
        for linkEachItem in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "p-title", " " ))]//a/@href').extract():
            print("1:"+self.domain+"/"+linkEachItem)
            # print("2:"+self.domain.urljoin(linkEachItem))
            yield scrapy.Request("https://" + self.domain+"/"+linkEachItem, callback=self.crawlDataRealEstate)

    def convertPriceToNumber(self, price):
        priceConverted = price
        if (len(price[0].split()) > 0):
            if (price[0].split()[1] == u'tỷ'):
                print(price[0].split()[0])
                priceConverted = float(price[0].split()[0]) * 1000000000
            elif (price[0].split()[1] == u'triệu'):
                print(price)
                print(price[0].split()[0])
                priceConverted = float(price[0].split()[0]) * 1000000
            else:
                priceConverted = None
        return [priceConverted]

    def crawlDataRealEstate(self, response):
        print("start crawl data real estate")
        type = response.css('.div-hold > .table-detail .row:nth-child(1) .right::text').extract()
        address = response.css('.div-hold > .table-detail .row:nth-child(2) .right::text').extract()

        numberBedrooms = response.css('#LeftMainContent__productDetail_roomNumber .right::text').extract()
        if (len(numberBedrooms) > 0):
            numberBedrooms = numberBedrooms[0].split()[0]

        numberToilets = response.css('#LeftMainContent__productDetail_toilet .right::text').extract()
        if (len(numberToilets) > 0):
            numberToilets = numberToilets[0].split()[0]

        price = response.css('.mar-right-15 strong::text').extract()
        price = self.convertPriceToNumber(price)
        area = [float(response.css('.mar-right-15+ .gia-title strong::text').extract()[0].split('m')[0].lstrip().rstrip())]
        longitude = response.css('#hdLong::attr(value)').extract()
        latitude = response.css('#hdLat::attr(value)').extract()
        nameOwner = response.css('#LeftMainContent__productDetail_contactName .right::text').extract()
        mobile = response.css('#LeftMainContent__productDetail_contactMobile .right::text').extract()
        email = response.css('#contactEmail a::text').extract()

        sizeFront = response.css('#LeftMainContent__productDetail_frontEnd .right::text').extract()
        if (len(sizeFront) >0):
            sizeFront = sizeFront[0].split()[0]

        numberFloors = response.css('#LeftMainContent__productDetail_floor .right::text').extract()
        if (len(numberFloors) > 0):
            numberFloors = numberFloors[0].split()[0]

        wardin = response.css('#LeftMainContent__productDetail_wardin .right::text').extract()
        if (len(wardin) > 0):
            wardin = wardin[0].split()[0]

        homeDirection = response.css('#LeftMainContent__productDetail_direction .right::text').extract()
        balconyDirection = response.css('#LeftMainContent__productDetail_balcony .right::text').extract()
        interior = response.css('#LeftMainContent__productDetail_interior .right::text').extract()
        projectSize = response.css('#LeftMainContent__productDetail_projectSize .right::text').extract()
        projectName = response.css('#project .row:nth-child(1) .right::text').extract()
        projectOwner = response.css('#LeftMainContent__productDetail_projectOwner .right::text').extract()
        codePost = response.css('.prd-more-info div div::text').extract()
        startDatePost = response.css('.prd-more-info div:nth-child(3)::text').extract()[-1]
        endDatePost = response.css('.prd-more-info div+ div::text').extract()[-1]
        typePost = response.css('.prd-more-info div+ div:nth-child(2)::text').extract()[-1]

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
        item['numberFloors'] = numberFloors
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

        yield item
