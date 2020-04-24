from rest_framework import serializers
from .models import RealEstate, News

class GetAllRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate
        # fields = ('idPost', 'price', 'area', 'title')
        # fields = ('title', 'price', 'content')
        fields = '__all__'
class GetAllNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'