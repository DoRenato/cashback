from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('type', 'value', 'qty')


class SaleAdmin(admin.ModelAdmin):
    pass



admin.site.register(ProductType)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
