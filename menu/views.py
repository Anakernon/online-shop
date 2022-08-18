from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateInfoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from .serializers import *
from .models import *
import random

class MenuView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu/carousel/main.html'
    
    serializer_class = MenuSerializer
    
    def post(self, request):
        request.session["session_location"] = request.POST.get("session-location")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    def get(self, request):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
            
        pic = random.randrange(0, 2)
        lastprod = Product.objects.latest("id")
        adv1 = Advertisment.objects.all()[0]
        adv2 = Advertisment.objects.latest("id")
        queryset = Menu.objects.all()
        return Response({'dataset': queryset, 
                                        "locationset" : Location.objects.all(), 
                                        "location" : request.session['session_location'],
                                        "pic" : pic,
                                        "ad" : lastprod,
                                        "adv1" : adv1,
                                        "adv2" : adv2
                                    })
    
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu/carousel/category.html'
 
    def post(self, request, **kwargs):
        request.session["session_location"] = request.POST.get("session-location")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    def get(self, request, category_link, format = None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
            
        if len(Menu.objects.filter(link = category_link)) > 0:
            queryset = Category.objects.filter(menu__link = category_link)
            serializer = CategorySerializer(queryset, many = True)
            return Response({"dataset" : serializer.data, 
                                            "locationset" : Location.objects.all(), 
                                            "location" : request.session['session_location']
                                        }, status = status.HTTP_200_OK)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND) #return Redirect("./")
    
class GroupView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu/carousel/group.html'
    
    def post(self, request, **kwargs):
        request.session["session_location"] = request.POST.get("session-location")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    def get(self, request, category_link, group_link, format = None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
            
        if len(Menu.objects.filter(link = category_link)) > 0:
            if len(Category.objects.filter(menu__link = category_link, link = group_link)) > 0:
                queryset = Group.objects.filter(category__menu__link = category_link, category__link = group_link)
                serializer = GroupSerializer(queryset, many = True)
                return Response({"dataset" : serializer.data, 
                                                "locationset" : Location.objects.all(), 
                                                "parent" :  Menu.objects.get(link=category_link),
                                                "location" : request.session['session_location']
                                            }, status = status.HTTP_200_OK)
            return Response("Group doesn't exist", status = status.HTTP_404_NOT_FOUND)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND)
    
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu/carousel/productlist.html'
    
    def post(self, request, **kwargs):

        if request.POST.get("session-location"):
            request.session["session_location"] = request.POST.get("session-location")
            
        if request.POST.get("add-item"):
            item = Product.objects.get(id = request.POST.get("add-item"))
            session = Session.objects.get(session_key=request.session.session_key)
            if not CartItem.objects.filter(session = session, product = item).count():
                cart_item = CartItem(session = session, product = item, quantity = 1)
                cart_item.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    def get(self, request, category_link, group_link, productlist_link, format = None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
            
        if len(Menu.objects.filter(link = category_link)) > 0:
            if len(Category.objects.filter(link = group_link)) > 0:
                if len(Group.objects.filter(category__menu__link = category_link, category__link = group_link, link = productlist_link)) > 0:
                    queryset = Product.objects.filter(group__category__menu__link = category_link, group__category__link = group_link, group__link = productlist_link, location__name = request.session["session_location"])
                    serializer = ProductSerializer(queryset, many = True)
                    return Response({"dataset" : serializer.data, 
                                                    "locationset" : Location.objects.all(), 
                                                    "parent" :  Menu.objects.get(link=category_link), 
                                                    "parent1" :  Category.objects.get(link=group_link),
                                                    "location" : request.session['session_location']
                                                }, status = status.HTTP_200_OK)
                return Response("Products doesn't exist", status = status.HTTP_404_NOT_FOUND)
            return Response("Group doesn't exist", status = status.HTTP_404_NOT_FOUND)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND)
    
class ProductView(APIView):
    serializer_class = ProductSerializer
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu/carousel/product.html'
    
    def post(self, request, **kwargs):
        request.session["session_location"] = request.POST.get("session-location")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    def get(self, request, category_link, group_link, productlist_link, product_link, format = None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
            
        if len(Menu.objects.filter(link = category_link)) > 0:
            if len(Category.objects.filter(link = group_link)) > 0:
                if len(Group.objects.filter(link = productlist_link)) > 0:
                    if len(Product.objects.filter(group__category__menu__link = category_link, group__category__link = group_link, group__link = productlist_link, link = product_link, location__name = request.session["session_location"])) > 0:
                        product = Product.objects.filter(group__category__menu__link = category_link, group__category__link = group_link, group__link = productlist_link, location__name = request.session["session_location"]).get(link = product_link)
                        serializer = ProductSerializer(product)
                        return Response({"data" : serializer.data, 
                                                        "locationset" : Location.objects.all(), 
                                                        "parent" :  Menu.objects.get(link=category_link), 
                                                        "parent1" :  Category.objects.get(link=group_link), 
                                                        "parent2" : Group.objects.get(link=productlist_link),
                                                        "location" : request.session['session_location']
                                                    }, status = status.HTTP_200_OK)
                    return Response("Product doesn't exist", status = status.HTTP_404_NOT_FOUND)
                return Response("Products doesn't exist", status = status.HTTP_404_NOT_FOUND)
            return Response("Group doesn't exist", status = status.HTTP_404_NOT_FOUND)
        return Response("Category doesn't exist", status = status.HTTP_404_NOT_FOUND)
    
class InfoView(APIView):
    serializer_class = InfoSerializer
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu/carousel/info.html'
    
    def get(self, request, format = None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
        
        info = Info.objects.latest("id")
        serializer = InfoSerializer(info)
        return Response({"data" : serializer.data,
                                        "locationset" : Location.objects.all(),
                                        "location" : request.session['session_location']
                                    }, status = status.HTTP_200_OK)
        
@login_required(login_url="/login")
@permission_required("menu.change_info", login_url="/login", raise_exception=True)
def update_info(request):
    if request.method == 'POST':
        form = UpdateInfoForm(request.POST, instance = Info.objects.latest("id"))
        if form.is_valid():
            info = form.save()
            return redirect("/info")
    else:
        form = UpdateInfoForm()
    return render(request, 'menu/carousel/info_update.html', {"form": form})
    
@api_view(['POST',"GET"])
def search(request):
    if not request.session.exists(request.session.session_key):
            request.session.create()
            request.session["session_location"] = Location.objects.get(pk=1).name
    
    if request.method == "POST":
        
        if request.POST.get("add-item"):
            item = Product.objects.get(id = request.POST.get("add-item"))
            session = Session.objects.get(session_key=request.session.session_key)
            if not CartItem.objects.filter(session = session, product = item).count():
                cart_item = CartItem(session = session, product = item, quantity = 1)
                cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        request.session["session_location"] = request.POST.get("session-location")

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), location__name = request.session["session_location"])
        serializer = ProductSerializer(products, many=True)
        return render(request, 'menu/carousel/search.html', {"dataset" : serializer.data, 
                                                                                                "locationset" : Location.objects.all(),
                                                                                                "location" : request.session['session_location']
                                                                                               })
    else:
        return render(request, 'menu/carousel/search.html', {"locationset" : Location.objects.all()})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/#')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

def cart(request):

    if not request.session.exists(request.session.session_key):
        request.session.create()
        request.session["session_location"] = Location.objects.get(pk=1).name 
        
    if request.method == "GET":
        session = Session.objects.get(session_key=request.session.session_key)
        if not Cart.objects.filter(session = session).count():
            cart = Cart(session = session, cost = 0, total_cost = 0)
            cart.save()
            
        cartdata = Cart.objects.get(session = session)
        items = CartItem.objects.filter(session = session)
        cartdata.items.set(items)
        cartdata.save()
        cartdata.count_cost()
        dataset = cartdata.items.all()

        return render(request, 'menu/carousel/cart.html', {"cartdata" : cartdata, 
                                                                                            "dataset" : dataset, 
                                                                                            "locationset" : Location.objects.all(),
                                                                                            "location" : request.session['session_location']
                                                                                            })        
            
    if request.method == "POST":
        
        if request.POST.get("increase-qty"):
            item = CartItem.objects.get(product = request.POST.get("increase-qty"))
            item.quantity = item.quantity + 1
            item.save()
            
        if request.POST.get("decrease-qty"):
            item = CartItem.objects.get(product = request.POST.get("decrease-qty"))
            if item.quantity > 1:
                item.quantity = item.quantity - 1
                item.save()
            else:
                item.delete()
                
        if request.POST.get("remove-item"):
            item = CartItem.objects.get(product = request.POST.get("remove-item"))
            item.delete()
            
        if request.POST.get("submit-cart"):
            return HttpResponseRedirect("http://127.0.0.1:8000/submit")
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))








