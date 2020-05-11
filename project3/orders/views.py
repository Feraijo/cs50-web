from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *



# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    # context = {
    #     "user": request.user
    # }
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

# CLASS_MAP = {
#         'Salad': [Salad],
#         'Pasta': [Pasta],
#         'Sub': [SubName, Sub],
#         'DinnerPlatter': [DinnerPlatterName, DinnerPlatter],
#         'Pizza': [PizzaType, PizzaTitle, Pizza],
#     }
CLASS_MAP = {
        'Salad': Salad,
        'Pasta': Pasta,
        'Sub': Sub,
        'DinnerPlatter': DinnerPlatter,
        'Pizza': Pizza,
    }

def get_add(request):
    type_id = request.POST["type_id"]
    print(type_id)
    sa = SubAddition.objects.values_list()
    sa = {x[0]: (x[1], x[3]) for x in sa}
    return JsonResponse(sa)

def menu_view(request, menu_id):
    res = {}    
    objs = CLASS_MAP[menu_id].objects.values().order_by('name')  
    if menu_id == 'Pizza':
        res.update({'pz_types':dict(PizzaType.objects.values_list())})
        res.update({'adds':dict(Topping.objects.values_list())})
    if menu_id == 'Sub':
        sa = SubAddition.objects.values_list()
        sa = {x[0]: (x[1], x[3]) for x in sa}        
        res.update({'adds':sa})
    #print(res)
    res.update({'objs':objs, 'menu_id':menu_id})
    return render(request, "orders/menu.html", res)
#     # if request.method == 'GET':
#     #     return render(request, "orders/menu.html", {'menu_id':menu_id})
#     # return jsonify({"success": True, 'sdf':'xcv'})
#     #objs = {x.__name__: x.objects.all() for x in CLASS_MAP[menu_id]}
#     #objs = [{'name': CLASS_MAP[menu_id].objects.filter(name_id=q['name']).first().name, 'prices':q['ar']} for q in \
#     #        [x for x in CLASS_MAP[menu_id].objects.values('name').annotate(ar=ArrayAgg('price'))]]
#     objs = CLASS_MAP[menu_id].objects
#     if menu_id in ['Salad','Pasta']:
#         res = objs.values('name').annotate(price=ArrayAgg('price'))
        
#         res = {objs.filter(name=row['name']).first().name: 
#                 row['price'] for row in res}
#         tp = 1
#     elif menu_id in ['Sub','DinnerPlatter']:
#         res = objs.values('name').annotate(price=ArrayAgg('price'), size=ArrayAgg('size'))
#         res = {objs.filter(name_id=row['name']).first().name: 
#                 {x[0]:x[1] for x in zip(row['size'], row['price'])} for row in res}
#         tp = 2
#     else:
#         res = objs.values('pizza_title', 'pizza_type').annotate(price=ArrayAgg('price'), 
#                 size=ArrayAgg('size')).order_by('pizza_type', 'pizza_title')        
#         res = {(PizzaType.objects.get(pk=row['pizza_type']), objs.filter(pizza_title=row['pizza_title']).first().pizza_title): 
#                 {x[0]:x[1] for x in zip(row['size'], row['price'])} for row in res}
#         print(res)
#         tp = 3
#     # res = {}
#     # for row in objs:
#     #     key = CLASS_MAP[menu_id].objects.filter(name_id=row['name']).first().name
#     #     prices = zip(row['size'], row['price'])
#     #     res[key] = prices
    
    
#     return render(request, "orders/menu.html", {'objs':res, 'menu_id':menu_id, 'type':tp})     # 
    