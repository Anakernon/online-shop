from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File

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
        return f"{self.link}/"
        
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
        return f"{self.link}/"
        
    def get_image(self):
        if self.image:
            return self.image.url[13:]
        return ""
        
class Product(models.Model):
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
        return f"{self.link}/"
        
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
