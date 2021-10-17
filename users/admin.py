from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'document', 'id')


admin.site.register(User)
admin.site.register(Customer, CustomerAdmin)