from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.contrib.sessions.models import Session

class Location(models.Model):
    name = models.CharField(max_length = 64, unique = True)
    
    def __str__(self):
        return self.name
    
class Menu(models.Model):
    name = models.CharField(max_length = 32, default = "Category name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "menu/static/menu/images/menu")
    order = models.IntegerField()
    
    class Meta:
        ordering = ("order",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.link}/"
        
    def get_image(self):
        if self.image:
            return self.image.url[13:]
        return ""
        
class Category(models.Model):
    menu = models.ForeignKey(Menu, related_name = "category", on_delete = models.CASCADE)
    name = models.CharField(max_length = 32, default = "Group name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "menu/static/menu/images/menu")
    order = models.IntegerField()
    
    class Meta:
        ordering = ("order",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.menu.link}/{self.link}/"
        
    def get_image(self):
        if self.image:
            return self.image.url[13:]
        return ""

class Group(models.Model):
    category = models.ForeignKey(Category, related_name = "group", on_delete = models.CASCADE)
    name = models.CharField(max_length = 32, default = "Products name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "menu/static/menu/images/menu")
    order = models.IntegerField()
    
    class Meta:
        ordering = ("order",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.category.menu.link}/{self.category.link}/{self.link}/"
        
    def get_image(self):
        if self.image:
            return self.image.url[13:]
        return ""
        
class Product(models.Model):
    location = models.ManyToManyField(Location)
    group = models.ForeignKey(Group, related_name = "product", on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, default = "Product name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "menu/static/menu/images/products")
    thumbnail = models.ImageField(upload_to = "menu/static/menu/images/products")
    description = models.TextField(blank = True, null = True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    date_added = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ("-date_added",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.group.category.menu.link}/{self.group.category.link}/{self.group.link}/{self.link}/"
        
    def get_image(self):
        if self.image:
            return self.image.url[13:]
        return ""
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url[13:]
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url[13:]
            else:
                return ""
                
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality = 95)
        thumbnail = File(thumb_io, name = image.name)
        return thumbnail
        
class Info(models.Model):
    name = models.CharField(max_length = 250)
    text = models.TextField(max_length = 5000)

class Advertisment(models.Model):
    title1 = models.CharField(max_length = 32)
    text1 = models.TextField(max_length = 128)
    link1 = models.URLField()
    picture1 = models.ImageField(upload_to = "menu/static/menu/images/ad")
    btn1 = models.CharField(max_length = 32, default = "Button")
    title2 = models.CharField(max_length = 32)
    text2 = models.TextField(max_length = 128)
    link2 = models.URLField()
    picture2 = models.ImageField(upload_to = "menu/static/menu/images/ad")
    btn2 = models.CharField(max_length = 32, default = "Button")
    
    def get_image1(self):
        if self.picture1:
            return self.picture1.url[13:]
        return ""
     
    def get_image2(self):
        if self.picture2:
            return self.picture2.url[13:]
        return ""
    
class CartItem(models.Model):
    session = models.ForeignKey(Session, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.product.name
        
    def total_cost(self):
        return self.quantity * self.product.price
    
class Cart(models.Model):
    session = models.ForeignKey(Session, on_delete = models.CASCADE)
    items = models.ManyToManyField(CartItem)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    total_cost = models.IntegerField(default = 0)
    
    def count_cost(self):
        pass
    
    
