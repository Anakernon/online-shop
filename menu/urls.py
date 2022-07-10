from django.urls import path
from .views import *

app_name = "menu"
urlpatterns = [
    path("<slug:menu_link>/", Menu.as_view(), name = "menu"), 
    path("<slug:menu_link>/<slug:category_link>/", Category.as_view(), name = "category"),
    path("<slug:menu_link>/<slug:category_link>/<slug:group_link>/", Group.as_view(), name = "group"),
    path("<slug:menu_link>/<slug:category_link>/<slug:group_link>/<slug:product_link>/", Product.as_view(), name = "product")
]