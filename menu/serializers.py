from rest_framework import serializers
from.models import *

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
        "id", 
        "name", 
        "get_absolute_url", 
        "get_image", 
        "order")
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
        "id", 
        "name", 
        "get_absolute_url", 
        "get_image", 
        "order")
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
        "id", 
        "name", 
        "get_absolute_url", 
        "get_image", 
        "order")
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
        "id", 
        "name", 
        "get_absolute_url",
        "description",
        "price",
        "get_image", 
        "get_thumbnail")
        
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ("id", "name", "text")