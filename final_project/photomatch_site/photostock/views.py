from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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

def login_view(request):
    if request.method == 'GET':
        return render(request, "photostock/login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'Successfully logged in.')
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, 'Invalid credentials.')
        return render(request, "photostock/login.html")


def logout_view(request):
    logout(request)
    #messages.error(request, 'Logged out.')
    return render(request, "photostock/login.html", {"messages": ("Logged out.",)})

def register_view(request):
    is_new = request.path == '/register'
    if request.method == 'GET':
        # GET        
        user_form = NewUserForm() if is_new else UserForm(instance=request.user)
        profile_form = ProfileForm() if is_new else ProfileForm(instance=request.user.profile)
        return render(request, 'photostock/profile.html', {
            'forms': (user_form, profile_form)
        })
    else:
        # POST

        # TODO registration form processing
        user_form = NewUserForm(request.POST) if is_new else UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():        
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile saved.')
            return HttpResponseRedirect(reverse("index"))            
        else:
            messages.error(request, (user_form.errors, profile_form.errors))
            return HttpResponseRedirect(reverse("register"))
            
        return HttpResponseRedirect(reverse("index"))
        # if is_new:
        #     username = request.POST["username"]
        #     password = request.POST["password"]
        #     first_name = request.POST["first_name"]
        #     last_name = request.POST["last_name"]
        #     email = request.POST["email"]
        #     user = User.objects.create_user(username, email, password)
        #     user.first_name = first_name
        #     user.last_name = last_name
        #     user.save()
        # else:
        #     user = request.user
        
        # profile_form = ProfileForm(request.POST, instance=user.profile)
        # if user_form.is_valid() and profile_form.is_valid():
        #     user_form.save()
        #     profile_form.save()
        #     messages.success(request, 'Profile saved.')
        #     return HttpResponseRedirect(reverse("index"))
        # else:
        #     messages.error(request, 'There were some errors in profile data.')
        #     return HttpResponseRedirect(reverse("register"))
