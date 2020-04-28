from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crawler.models import RealEstate
import turicreate as tc
import numpy
import json
from crawler.serializers import GetAttributeRegression
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

class GetResultRegression(APIView):
    def get(self, request):
        
        top_id = RealEstate.objects.values_list('idCrawlerJob', flat=True).distinct()
        list_reo = RealEstate.objects.filter(price__gt = 0, 
            area__gt = 0, numberBedrooms__gt = 0, numberToilets__gt = 0, numberFloor__gt =0)
        # vlqs = list_reo.values_list()
        # r = numpy.core.records.fromrecords(vlqs, names=[f.name for f in RealEstate._meta.fields])

        mydata = GetAttributeRegression(list_reo, many = True)

        # json_string = json.dumps([ob.__dict__ for ob in mydata.data])

        # configFile = open((BASE+'/data.json'))
        # json.dump(mydata.data, 'tuan.json')
        # tuan = json.dump(mydata.data)

        # numpy_array = numpy.array(list(mydata.data))
        # l=[1,2,3]
        # sf = tc.SFrame(numpy_array)

        # data = turicreate.SFrame.read_json(mydata.data)
        # done
        # sf = turicreate.SFrame.read_json(BASE+'/data.json')

        i = 1
        i+=1
        return Response(data=mydata.data, status=status.HTTP_200_OK)
