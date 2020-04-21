from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealEstateObject, News
from .serializers import GetAllRealEstateObjectSerializer, GetAllNewsSerializer
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

class GetDataAPIView(APIView):
    def sendRequestCrawl(self, typeSpider):
        if (typeSpider == 'reo'):
            configFile = open((BASE+'/config/reoconfig.json'))
        if (typeSpider == 'news'):
            configFile = open((BASE+'/config/newsconfig.json'))
        configData = json.load(configFile)
        unique_id = str(uuid4())

        settings = {
            'unique_id': unique_id, 
            'type': typeSpider,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        listTask = []
        if (typeSpider == 'reo'):
            for reo in configData:
                url = reo['url']
                domain = urlparse(url).netloc 
                task = scrapyd.schedule('default', 'realestateobjectcrawl', 
                    settings=settings, url=url, domain=domain, config = json.dumps(reo))
                listTask.append(task)
        if (typeSpider == 'news'):
            for news in configData:
                url = news['url']
                domain = urlparse(url).netloc 
                task = scrapyd.schedule('default', 'newscrawl', 
                    settings=settings, url=url, domain=domain, config = json.dumps(news))
                listTask.append(task)
        
        for task in listTask:
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
            unique_id = self.sendRequestCrawl(typeSpider)
        myData = None
        
        if (typeSpider == 'reo'):
            if (daily == 'true'):
                now = datetime.datetime.now()
                list_reo = RealEstateObject.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day)
            else:
                if (unique_id != None):
                    list_reo = RealEstateObject.objects.filter(idCrawlerJob=unique_id)
                else:
                    list_reo = RealEstateObject.objects.all()

            mydata = GetAllRealEstateObjectSerializer(list_reo, many = True)
        elif (typeSpider == 'news'):
            if (daily == 'true'):
                now = datetime.datetime.now()
                list_news = News.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day)
            else:
                if (unique_id != None):
                    list_news = News.objects.filter(idCrawlerJob=unique_id)
                else:
                    list_news = News.objects.all()
            
            mydata = GetAllNewsSerializer(list_news, many = True)

        if (mydata is None):
            return Response(status = status.HTTP_404_NOT_FOUND)

        return Response(data = mydata.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        typeSpider = request.data.get('type', None)
        if (typeSpider == 'reo'):
            configFile = open((BASE+'/config/reoconfig.json'))
        if (typeSpider == 'news'):
            configFile = open((BASE+'/config/newsconfig.json'))
        
        configData = json.load(configFile)
        unique_id = str(uuid4())
        settings = {
            'unique_id': unique_id, 
            'type': typeSpider,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        if (typeSpider == 'reo'):
            for reo in configData:
                url = reo['url']
                domain = urlparse(url).netloc 
                task = scrapyd.schedule('default', 'realestateobjectcrawl', 
                    settings=settings, url=url, domain=domain, config = json.dumps(reo))
        if (typeSpider == 'news'):
            for news in configData:
                url = news['url']
                domain = urlparse(url).netloc 
                task = scrapyd.schedule('default', 'newscrawl', 
                    settings=settings, url=url, domain=domain, config = json.dumps(news))
        
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })

