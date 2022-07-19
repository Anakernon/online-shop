from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.shortcuts import render



def index(request, *args, **kwargs):
    return render(request, 'menu/index.html')

class MenuView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 
    def get(self, request, category_link, format = None):
        if len(Menu.objects.filter(link = category_link)) > 0:
            queryset = Category.objects.filter(menu__link = category_link)
            serializer = CategorySerializer(queryset, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND) #return Redirect("./")
    
    

class GroupView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    def get(self, request, category_link, group_link, format = None):
        if len(Menu.objects.filter(link = category_link)) > 0:
            if len(Category.objects.filter(menu__link = category_link, link = group_link)) > 0:
                queryset = Group.objects.filter(category__menu__link = category_link, category__link = group_link)
                serializer = GroupSerializer(queryset, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response("Group doesn't exist", status = status.HTTP_404_NOT_FOUND)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND)
    
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self, request, category_link, group_link, productlist_link, format = None):
        if len(Menu.objects.filter(link = category_link)) > 0:
            if len(Category.objects.filter(link = group_link)) > 0:
                if len(Group.objects.filter(category__menu__link = category_link, category__link = group_link, link = productlist_link)) > 0:
                    queryset = Product.objects.filter(group__category__menu__link = category_link, group__category__link = group_link, group__link = productlist_link)
                    serializer = ProductSerializer(queryset, many = True)
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response("Products doesn't exist", status = status.HTTP_404_NOT_FOUND)
            return Response("Group doesn't exist", status = status.HTTP_404_NOT_FOUND)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND)
    
class ProductView(APIView):
    serializer_class = ProductSerializer
    
    def get(self, request, category_link, group_link, productlist_link, product_link, format = None):
        if len(Menu.objects.filter(link = category_link)) > 0:
            if len(Category.objects.filter(link = group_link)) > 0:
                if len(Group.objects.filter(link = productlist_link)) > 0:
                    if len(Product.objects.filter(group__category__menu__link = category_link, group__category__link = group_link, group__link = productlist_link, link = product_link)) > 0:
                        product = Product.objects.filter(group__category__menu__link = category_link, group__category__link = group_link, group__link = productlist_link).get(link = product_link)
                        serializer = ProductSerializer(product)
                        return Response(serializer.data, status = status.HTTP_200_OK)
                    return Response("Product doesn't exist", status = status.HTTP_404_NOT_FOUND)
                return Response("Products doesn't exist", status = status.HTTP_404_NOT_FOUND)
            return Response("Group doesn't exist", status = status.HTTP_404_NOT_FOUND)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND)
    
class InfoView(APIView):
    serializer_class = InfoSerializer
    def get(self, request, format = None):
        info = Info.objects.filter(id=2)
        serializer = InfoSerializer(info, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
        
class DeliveryView(APIView):
    serializer_class = InfoSerializer
    def get(self, request, format = None):
        info = Info.objects.filter(id=1)
        serializer = InfoSerializer(info, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
