from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File

SITE_ADDR = "localhost:8000"
class Menu(models.Model):
    name = models.CharField(max_length = 32, default = "Category name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "images/menu")
    order = models.IntegerField(unique = True, required = True)
    
    class Meta:
        ordering = ("order",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.link}/"
        
    def get_image(self):
        if self.image:
            return SITE_ADDR + self.image.url
        return ""
        
class Category(models.Model):
    menu = models.ForeignKey(Menu, related_name = "category", on_delete = models.CASCADE)
    name = models.CharField(max_length = 32, default = "Group name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "images/menu")
    order = models.IntegerField(unique = True, required = True)
    
    class Meta:
        ordering = ("order",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.menu.link}/{self.link}/"
        
    def get_image(self):
        if self.image:
            return SITE_ADDR + self.image.url
        return ""

class Group(models.Model):
    category = models.ForeignKey(Category, related_name = "group", on_delete = models.CASCADE)
    name = models.CharField(max_length = 32, default = "Products name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "images/menu")
    order = models.IntegerField(unique = True, required = True)
    
    class Meta:
        ordering = ("order",)
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"{self.category.menu.link}/{self.category.link}/{self.link}/"
        
    def get_image(self):
        if self.image:
            return SITE_ADDR + self.image.url
        return ""
        
class Product(models.Model):
    group = models.ForeignKey(Group, related_name = "product", on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, default = "Product name", unique = True)
    link = models.SlugField(unique = True)
    image = models.ImageField(upload_to = "images/products")
    thumbnail = models.ImageField(upload_to = "images/products")
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
            return SITE_ADDR + self.image.url
        return ""
    
    def get_thumbnail(self):
        if self.thumbnail:
            return SITE_ADDR + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return SITE_ADDR + self.thumbnail.url
            else:
                return: ""
                
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality = 95)
        thumbnail = File(thumb_io, name = image.name)
        return thumbnail
        
class Info(models.Model):
    name = models.CharField()
    text = models.TextField()