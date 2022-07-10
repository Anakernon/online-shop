from django.shortcuts import render
from rest.framework import generics
from .serializers import *
from .models import *

class MenuView(generics.ListView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
class CategoryView(generics.ListView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class GroupView(generics.ListView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class ProductView(APIView):
    def get_object(self, group_link, product_link):
        try:
            return Product.objects.filter(group__link=group_link).get(link=product_link)
        except Product.DoesNotExist:
            return Http404
            
    def get(self, request, group_link, product_link, format=None):
        product = self.get_object(group_link, product_link)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class InfoView(generics.View):
    queryset = Info.objects.all()
    serializer_class =InfoSerializer