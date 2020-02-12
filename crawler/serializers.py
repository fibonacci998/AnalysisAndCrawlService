from rest_framework import serializers
from .models import RealEstateObject, Employee

class GetAllRealEstateObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateObject
        fields = ('idPost', 'price', 'area')
        # fields = ('title', 'price', 'content')

class GetAllEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'title', 'price', 'content')

class EmployeeSerializer(serializers.Serializer):
    title1 = serializers.CharField(max_length=50)
    price1 = serializers.IntegerField()
    content1 = serializers.CharField(max_length=50)

