from django.urls import path
from .views import *

app_name = "menu"
urlpatterns = [
    path("", MenuView.as_view(), name = "menu"), 
    path("stat/", stat, name = "stat"), 
    path("info/", InfoView.as_view(), name = "info"),
    path('info/update', update_info, name='update_info'),
    path('search/', search, name = "search"),
    path('sign-up/', sign_up, name='sign_up'),
    path('cart/', cart, name='cart'),    
    path("profile/", profile, name = "profile"),
    path("<slug:category_link>/", CategoryView.as_view(), name = "category"),
    path("<slug:category_link>/<slug:group_link>/", GroupView.as_view(), name = "group"),
    path("<slug:category_link>/<slug:group_link>/<slug:productlist_link>/", ProductListView.as_view(), name = "productlist"),
    path("<slug:category_link>/<slug:group_link>/<slug:productlist_link>/<slug:product_link>/", ProductView.as_view(), name = "product")
]
