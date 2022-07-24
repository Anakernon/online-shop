from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateInfoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .serializers import *
from .models import *


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
        info = Info.objects.get(id=2)
        serializer = InfoSerializer(info)
        return Response(serializer.data, status = status.HTTP_200_OK)
        
@login_required(login_url="/login")
@permission_required("menu.update_info", login_url="/login", raise_exception=True)
def update_info(request):
    if request.method == 'PATCH':
        form = UpdateInfoForm(request.PATCH)
        if form.is_valid():
            info = form.save(commit=False)
            info.save()
            return redirect("/info")
    else:
        form = UpdateInfoForm()

    return render(request, 'info/update_info.html', {"form": form})
    
@api_view(['POST'])
def search(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('./')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
