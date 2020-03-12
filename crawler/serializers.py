from rest_framework import serializers
from .models import RealEstateObject, Employee, Quote

class GetAllRealEstateObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateObject
        # fields = ('idPost', 'price', 'area', 'title')
        # fields = ('title', 'price', 'content')
        fields = '__all__'

class GetAllEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'title', 'price', 'content')

class EmployeeSerializer(serializers.Serializer):
    title1 = serializers.CharField(max_length=50)
    price1 = serializers.IntegerField()
    content1 = serializers.CharField(max_length=50)

class GetQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('unique_id', 'text', 'author')
        # fields = ('title', 'price', 'content')

