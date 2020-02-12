from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealEstateObject,Employee
from .serializers import GetAllRealEstateObjectSerializer,GetAllEmployeeSerializer
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
from urllib.parse import urlparse
import os
scrapyd = ScrapydAPI('http://0.0.0.0:'+str(os.environ.get("PORT", 6800)))
# Create your views here.
def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False

    return True

# @csrf_exempt
class GetAllRealEstateObjectAPIView(APIView):
    def get(self, request):
        list_reo = RealEstateObject.objects.all()
        mydata = GetAllRealEstateObjectSerializer(list_reo, many = True)

        list_emp = GetAllEmployeeSerializer(Employee.objects.all(), many = True)
        return Response(data = mydata.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        # RealEstateObject.objects.create(title=, content=, price=)
        print("Go post")
        url = request.data.get('url', None) # take url comes from client. (From an input may be?)

        if not url:
            return JsonResponse({'error': 'Missing  args'})
        
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID. 
        
        # This is the custom settings for scrapy spider. 
        # We can send anything we want to use it inside spiders and pipelines. 
        # I mean, anything
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        print("creating crawler")
        # Here we schedule a new crawling task from scrapyd. 
        # Notice that settings is a special argument name. 
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        task = scrapyd.schedule('default', 'realestateobjectcrawl', 
            settings=settings, url=url, domain=domain)
        print("Created crawler")
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
