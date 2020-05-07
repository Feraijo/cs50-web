from django.http import HttpResponse
from django.shortcuts import render

from .models import Pizza

# Create your views here.
def index(request):
    context = {
        "menuitems": Pizza.objects.all()
    }
    return render(request, "orders/index.html", context)
