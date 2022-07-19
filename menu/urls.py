from django.urls import path
from .views import *

app_name = "menu"
urlpatterns = [
    path('', index, name=''),
    path("menu/", MenuView.as_view(), name = "menu"), 
    path("info/", InfoView.as_view(), name = "info"),
    path("delivery/", DeliveryView.as_view(), name = "delivery"),
    path('search/', search, name = "search"),
    path("menu/<slug:category_link>/", CategoryView.as_view(), name = "category"),
    path("menu/<slug:category_link>/<slug:group_link>/", GroupView.as_view(), name = "group"),
    path("menu/<slug:category_link>/<slug:group_link>/<slug:productlist_link>/", ProductListView.as_view(), name = "productlist"),
    path("menu/<slug:category_link>/<slug:group_link>/<slug:productlist_link>/<slug:product_link>/", ProductView.as_view(), name = "product")
]
