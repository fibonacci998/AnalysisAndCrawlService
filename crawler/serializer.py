from rest_framework import serializers
from .models import RealEstateObject

class GetAllRealEstateObjectSerializer(serializers.Serializer):
    class Meta:
        model = RealEstateObject
        # fields = ('idPost', 'price', 'area')
        # fields = '__all__'