from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crawler.models import RealEstate
import turicreate as tc
from math import log
import numpy as np
import json
from crawler.serializers import GetAttributeRegression, GetAllRealEstateSerializer
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

class GetPrice(APIView):

    reo = tc.SFrame(BASE+'/data_sframe')
    model = tc.load_model(BASE+'/model_3')

    def get(self, request):
        numberBedrooms = self.getValueFromGet(request, 'numberBedrooms')
        numberToilets = self.getValueFromGet(request, 'numberToilets')
        area = self.getValueFromGet(request, 'area')
        longitude = self.getValueFromGet(request, 'longitude')
        latitude = self.getValueFromGet(request, 'latitude')
        bedrooms_squared = numberToilets ** 2
        bed_bath_rooms = numberBedrooms * numberToilets
        log_sqft_living = log(area)
        lat_plus_long = longitude + latitude

        test_object = {
            'numberBedrooms' : [numberBedrooms],
            'numberToilets': [numberToilets],
            'area': [area],
            'longitude':[longitude],
            'latitude':[latitude],
            'bedrooms_squared': [bedrooms_squared],
            'bed_bath_rooms': [bed_bath_rooms],
            'log_sqft_living':[log_sqft_living],
            'lat_plus_long':[lat_plus_long],
        }


        predictValue = self.model.predict(tc.SFrame(test_object))[0]

        # top_id = RealEstate.objects.values_list('idCrawlerJob', flat=True).distinct()
        # list_reo = RealEstate.objects.filter(price__gt = 0, 
        #     area__gt = 0, numberBedrooms__gt = 0, numberToilets__gt = 0, numberFloor__gt =0, idCrawlerJob__in=top_id[:100])
        # list_reo = RealEstate.objects.all()

        # vlqs = list_reo.values_list()
        # r = numpy.core.records.fromrecords(vlqs, names=[f.name for f in RealEstate._meta.fields])

        # mydata = GetAttributeRegression(list_reo, many = True)

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

        # test = tc.SFrame(mydata.data)

    
        return Response(data=predictValue, status=status.HTTP_200_OK)
    
    def post(self, request):
        price = self.getValueFromPost(request, 'price')
        numberFloor = self.getValueFromPost(request, 'numberFloor')
        codePost = self.getValueFromPost(request, 'codePost')
        sizeFront = self.getValueFromPost(request, 'sizeFront')
        wardin = self.getValueFromPost(request, 'wardin')
        numberBedrooms = self.getValueFromPost(request, 'numberBedrooms')
        numberToilets = self.getValueFromPost(request, 'numberToilets')
        area = self.getValueFromPost(request, 'area')
        longitude = self.getValueFromPost(request, 'longitude')
        latitude = self.getValueFromPost(request, 'latitude')
        test_object = {
            'codePost': [int(codePost)],
            'price': [int(price)],
            'numberFloor': [int(numberFloor)],
            'numberBedrooms' : [numberBedrooms],
            'numberToilets': [numberToilets],
            'area': [area],
            'longitude':[longitude],
            'latitude':[latitude],
            'sizeFront':[sizeFront],
            'wardin':[wardin]
        }

        sframe = tc.SFrame(test_object)
        self.reo.append(sframe)
        self.reo.save(BASE+'/data_sframe')

        return Response(data="done", status=status.HTTP_200_OK)

    
    def transform_value(self, value, field):
        if (value == -1 or value == 0):
            return self.reo[(self.reo[field] != -1) & (self.reo[field] != 0)][field].mean()
        else:
            return value
    def getValueFromGet(self, request, field):
        try:
            value = float(request.GET[field])
        except:
            value = -1
            value = self.transform_value(value, field)
        return value
    def getValueFromPost(self, request, field):
        try:
            value = float(request.data[field])
        except:
            value = -1
            value = self.transform_value(value, field)
        return value
    