from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Register your models here.
from .models import *

class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change and obj.finished:
            send_mail(
                'Pizza Time! Order status',
                'Your order is ready.',
                'from@example.com',
                [obj.user.email],
                fail_silently=False,
            )
        super().save_model(request, obj, form, change)

admin.site.register(Purchase)
admin.site.register(MenuItem)
admin.site.register(Addition)
admin.site.register(AddType)
admin.site.register(ItemType)
admin.site.register(Order, OrderAdmin)
