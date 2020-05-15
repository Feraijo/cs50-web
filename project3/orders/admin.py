from django.contrib import admin
import sys, inspect

# Register your models here.
from .models import *

# class PizzaAdmin(admin.ModelAdmin):
#     fields = ('pizza_type', 'name',rice')

admin.site.register(Purchase)
admin.site.register(MenuItem)
admin.site.register(Addition)
admin.site.register(AddType)
admin.site.register(ItemType)
admin.site.register(Order)
