from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealEstateObject,Employee, Quote
from .serializers import GetAllRealEstateObjectSerializer,GetAllEmployeeSerializer, GetQuoteSerializer
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from django.http import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
from urllib.parse import urlparse
import os
import json
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))
import datetime

scrapyd = ScrapydAPI('http://0.0.0.0:'+str(os.environ.get("PORT", 6800)))
# Create your views here.
def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False

    return True


class GetAllRealEstateObjectAPIView(APIView):
    def sendRequestCrawl(self):
        configFile = open((BASE+'/config/reoconfig.json'))
        configData = json.load(configFile)
        temp = json.dumps(configData)

        url = configData['url']
        domain = urlparse(url).netloc 
        unique_id = str(uuid4())

        settings = {
            'unique_id': unique_id, 
            'type': 'reo',
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        task = scrapyd.schedule('default', 'realestateobjectcrawl', 
            settings=settings, url=url, domain=domain, config = temp)
        while(scrapyd.job_status('default',task) != 'finished'):
            pass
        return unique_id

    def getValueFromGet(self, request, attribute):
        try:
            value = request.GET[attribute]
        except:
            value = None
        return value
    def get(self, request):
        unique_id = request.data.get('unique_id', None)
        typeSpider = request.data.get('type', None)

        typeSpider = self.getValueFromGet(request, 'type')
        daily = self.getValueFromGet(request, 'daily')
        crawlnow = self.getValueFromGet(request, 'crawlnow')
        if (crawlnow == 'true'):       
            unique_id = self.sendRequestCrawl()
        myData = None
        
        if (daily == 'true'):
            now = datetime.datetime.now()
            list_reo = RealEstateObject.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day)

            # list_reo = RealEstateObject.objects.all()

            # top_dates = RealEstateObject.objects.order_by('-date').values_list('date', flat=True).distinct()
            # list_reo = RealEstateObject.objects.order_by('-date').filter(date__in=top_dates[:1])

            mydata = GetAllRealEstateObjectSerializer(list_reo, many = True)

        elif (typeSpider == 'reo'):
            # list_reo = RealEstateObject.objects.all()
            list_reo = RealEstateObject.objects.filter(idCrawlerJob=unique_id)
            # top_prices = RealEstateObject.objects.order_by('price').values_list('price', flat=True).distinct()
            # list_reo = RealEstateObject.objects.order_by('price').filter(price__in=top_prices[:10])

            mydata = GetAllRealEstateObjectSerializer(list_reo, many = True)

        # if (typeSpider == 'quote'):
        #     list_quote = Quote.objects.filter(unique_id = unique_id)
        #     mydata = GetQuoteSerializer(list_quote, many = True)
        if (mydata is None):
            return Response(status = status.HTTP_404_NOT_FOUND)

        return Response(data = mydata.data, status = status.HTTP_200_OK)
    
    def post(self, request):

        configFile = open((BASE+'/config/reoconfig.json'))
        configData = json.load(configFile)
        temp = json.dumps(configData)

        url = configData['url']
        typeSpider = request.data.get('type', None)

        domain = urlparse(url).netloc 
        unique_id = str(uuid4())

        settings = {
            'unique_id': unique_id, 
            'type': typeSpider,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        if (typeSpider == 'reo'):
            task = scrapyd.schedule('default', 'realestateobjectcrawl', 
                settings=settings, url=url, domain=domain, config = temp)
        if (typeSpider == 'quote'):
            task = scrapyd.schedule('default', 'toscrape-css', 
                settings=settings, url=url, domain=domain)
        while(scrapyd.job_status('default',task) == 'running'):
            pass

        
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })