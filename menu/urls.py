from django.urls import path
from .views import *

app_name = "menu"
urlpatterns = [
    path("", MenuView.as_view(), name = "menu"), 
    path("<slug:category_link>/", CategoryView.as_view(), name = "category"),
    path("<slug:category_link>/<slug:group_link>/", GroupView.as_view(), name = "group"),
    path("<slug:category_link>/<slug:group_link>/<slug:product_link>/", ProductView.as_view(), name = "product")
]
