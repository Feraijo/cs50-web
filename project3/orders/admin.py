from django.contrib import admin
import sys, inspect

# Register your models here.
from .models import *

# class PizzaAdmin(admin.ModelAdmin):
#     fields = ('pizza_type', 'name',rice')

admin.site.register(DinnerPlatter)
admin.site.register(Pasta)
admin.site.register(Pizza)
admin.site.register(PizzaType)
admin.site.register(Salad)
admin.site.register(Sub)
admin.site.register(SubAddition)
admin.site.register(Topping)
