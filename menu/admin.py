from django.contrib import admin
from .models import *

admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Info)
admin.site.register(Location)
admin.site.register(Advertisment)
admin.site.register(CartItem) #DELETE B4 PRODUCTION
admin.site.register(Cart) #DELETE B4 PRODUCTION

class Locs(admin.ModelAdmin):
    filter_horizontal = ("location",)
    
admin.site.register(Product, Locs)
