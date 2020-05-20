from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": None})
    context = {        
        "user": request.user
    }
    return HttpResponse("Hello, world. You're at the matcher index.")
    #render(request, "index.html", context)