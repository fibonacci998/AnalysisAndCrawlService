from rest_framework import serializers
from .models import RealEstateObject, News

class GetAllRealEstateObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateObject
        # fields = ('idPost', 'price', 'area', 'title')
        # fields = ('title', 'price', 'content')
        fields = '__all__'
class GetAllNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'