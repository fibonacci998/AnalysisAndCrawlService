from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealEstateObject
from .serializer import GetAllRealEstateObjectSerializer
# Create your views here.

class GetAllRealEstateObjectAPIView(APIView):
    def get(self, request):
        list_reo = RealEstateObject.objects.all()
        mydata = GetAllRealEstateObjectSerializer(list_reo, many = True)

        return Response(data = mydata.data, status = status.HTTP_200_OK)
