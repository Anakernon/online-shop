from django.contrib import admin
from .models import *

admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Info)
admin.site.register(Location)

class Locs(admin.ModelAdmin):
    filter_horizontal = ("location",)
    
admin.site.register(Product, Locs)
