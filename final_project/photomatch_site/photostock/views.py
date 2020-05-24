from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import HumanSerializer
from .models import Human

def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": None})
    context = {        
        "user": request.user
    }
    return render(request, "photostock/index.html", context)

class HumanViewSet(viewsets.ModelViewSet):
    queryset = Human.objects.all().order_by('second_name')
    serializer_class = HumanSerializer