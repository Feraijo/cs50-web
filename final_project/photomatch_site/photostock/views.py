from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": None})
    context = {        
        "user": request.user
    }
    return render(request, "photostock/index.html", context)