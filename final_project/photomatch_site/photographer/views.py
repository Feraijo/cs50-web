from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *
from .models import *

def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": None})
    context = {        
        "user": request.user
    }
    return HttpResponse("Hello, world. You're at the matcher index.")
    #render(request, "index.html", context)




class HumanViewSet(viewsets.ModelViewSet):
    queryset = Human.objects.all().order_by('second_name')
    serializer_class = HumanSerializer