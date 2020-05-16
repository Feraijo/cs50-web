from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *

def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {        
        "user": request.user
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def register_view(request): 
    if request.method == 'GET':
        return render(request, "orders/register.html", {"message": None })    
    username = request.POST["username"]
    password = request.POST["password"]   
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return render(request, "orders/login.html", {"message": 'Log in now with your login and password'})


def place_order(request):
    order = Order(user=request.user)
    order.save()
    for purch in request.user.purchases.pp():
        purch.pending = False
        purch.save()
        order.purchases.add(purch)
    context = {        
        "user": request.user
    }
    return render(request, "orders/index.html", context)

def cart_view(request):
    context = { 
        "user": request.user
    }
    if request.method == 'POST':        
        remove = request.POST["remove"]
        if remove == 'true':
            p = Purchase.objects.get(id=request.POST["id"])
            p.delete()
            return JsonResponse({'message':'purchase removed'})
        else:
            type_id = request.POST["type"]                
            size = request.POST["size"]
            adds = request.POST["adds"]
            amount = int(request.POST["amount"])
            mi = MenuItem.objects.get(id=request.POST["id"])
            p = Purchase(user=request.user, item=mi)
            p.save()
            if adds:
                for a in Addition.objects.filter(id__in=[int(x) for x in adds.split(',')]):
                    p.adds.add(a)
            if mi.price_small and mi.price_large:
                p.notes = size
            if size == 'Small':
                price = mi.price_small
            else:
                price = mi.price_large
            if type_id == 'Subs':
                for add in p.adds.all():
                    if add.price:
                        price += add.price
                    else:
                        price += 0.5
            p.amount = amount
            p.total_price = price * amount
            p.save()
            return JsonResponse({'message':'purchase added'})
    else:
        purchs = request.user.purchases.pp().order_by('id')
        context.update({'cart': purchs})
        return render(request, "orders/cart.html", context)

def menu_view(request, menu_id):
    res = {}
    if menu_id == 'Pizza':
        types = ItemType.objects.filter(name__endswith=menu_id)
        add_type = AddType.objects.get(name='Toppings')
        res.update({'adds': Addition.objects.filter(add_type=add_type)})
    elif menu_id == 'Subs':
        types = ItemType.objects.filter(name=menu_id)
        add_type = AddType.objects.get(name='SubAdditions')
        res.update({'adds': Addition.objects.filter(add_type=add_type)})
    else:
        types = ItemType.objects.filter(name=menu_id)
    objs = MenuItem.objects.filter(item_type__in=types).order_by('item_type' ,'name')
    
    res.update({'objs':objs, 'menu_id':menu_id})
    return render(request, "orders/menu.html", res)
