from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crawler.models import RealEstate
import turicreate

class GetResultRegression(APIView):
    def get(self, request):
        
        list_reo = RealEstate.objects.all()
        data = turicreate.SFrame(data=list_reo)
        return Response(data=data, status=status.HTTP_200_OK)
