from django.db import models
from django.contrib.auth.models import User

class b4Q(models.Model):
    user_name = models.CharField(max_length = 100)
    user_id = models.IntegerField()
    user_phone = models.CharField(max_length = 13)
    user_email = models.EmailField()
    user_address = models.CharField(max_length = 200)
    cart_id = models.IntegerField()
    product_names = models.TextField(max_length = 3200)
    product_prices = models.TextField(max_length = 320)
    product_quantities = models.TextField(max_length = 100)
    paid_amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['date_created',]

class OrderInQueue(models.Model):
    user_name = models.CharField(max_length = 100)
    user_id = models.IntegerField()
    user_phone = models.CharField(max_length = 13)
    user_email = models.EmailField()
    user_address = models.CharField(max_length = 200)
    cart_id = models.IntegerField()
    product_names = models.TextField(max_length = 3200)
    product_prices = models.TextField(max_length = 320)
    product_quantities = models.TextField(max_length = 100)
    paid_amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['date_created',]
    
    
class CompleteOrder(models.Model):
    user_name = models.CharField(max_length = 100)
    user_id = models.IntegerField()
    user_phone = models.CharField(max_length = 13)
    user_email = models.EmailField()
    user_address = models.CharField(max_length = 200)
    cart_id = models.IntegerField()
    product_names = models.TextField(max_length = 3200)
    product_prices = models.TextField(max_length = 320)
    product_quantities = models.TextField(max_length = 100)
    paid_amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-date_created',]
        
    def __str__(self):
        return self.date_created + "- $" + self.paid_amount
        
class extensions(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length = 13, default = "88005553535")
    address = models.CharField(max_length = 200, default = "USA")
    
    
    
    
    
    
        
        
