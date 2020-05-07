from django.contrib import admin
import sys, inspect

# Register your models here.
from .models import *

class PizzaAdmin(admin.ModelAdmin):
    fields = ('pizza_type', 'pizza_title', 'size', 'price')

admin.site.register(DinnerPlatter)
admin.site.register(DinnerPlatterName)
admin.site.register(Pasta)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(PizzaTitle)
admin.site.register(PizzaType)
admin.site.register(Salad)
admin.site.register(Size)
admin.site.register(Sub)
admin.site.register(SubAddition)
admin.site.register(SubName)
admin.site.register(Topping)


