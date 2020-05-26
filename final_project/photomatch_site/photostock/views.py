from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework import viewsets

#from .serializers import HumanSerializer
from .models import *

@login_required(redirect_field_name='')
def index(request):    
    context = {        
        "user": request.user
    }
    return render(request, "photostock/index.html", context)

def my_view(request, id): 
    instance = get_object_or_404(MyModel, id=id)
    form = MyForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('next_view')
    return render(request, 'my_template.html', {'form': form}) 

def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'You\'ve successfully updated the profile.')
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'There were some errors in profile data.')
            return HttpResponseRedirect(reverse("profile"))
        
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'photostock/profile.html', {
            'forms': (user_form, profile_form)
        })

def login_view(request):
    if request.method == 'GET':
        return render(request, "photostock/login.html", {"message": "Invalid credentials."})
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "photostock/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "photostock/login.html", {"message": "Logged out."})

def register_view(request): 
    print(request.method)
    if request.method == 'GET':
        return render(request, "photostock/register.html", {"message": None })    
    username = request.POST["username"]
    password = request.POST["password"]   
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return render(request, "photostock/login.html", {"message": 'Log in now with your login and password'})

# class HumanViewSet(viewsets.ModelViewSet):
#     queryset = Human.objects.all().order_by('second_name')
#     serializer_class = HumanSerializer