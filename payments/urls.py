from django.urls import path
from .views import *

app_name = "payments"
urlpatterns = [
    path("", submit, name = "submit"),
    path("stripe-webhook/", stripe_webhook, name = "stripe_webhook")
]
