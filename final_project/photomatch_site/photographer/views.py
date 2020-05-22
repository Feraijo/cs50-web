from django.shortcuts import render

def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": None})
    context = {        
        "user": request.user
    }
    return HttpResponse("Hello, world. You're at the matcher index.")
    #render(request, "index.html", context)