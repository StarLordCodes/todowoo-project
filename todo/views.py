from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, "todo/home.html", {"page_name": "Home page"})


def signupuser(request):
    # check if it's a get or POST request, POST means we have to create a user from the
    # submiited UserCreationForm, if its get request we have to provide the form to
    # the user
    if request.method == 'GET':
        return render(request, "todo/signupuser.html", {"form": UserCreationForm, "page_name": "Signup page"})
    else:
        # we have to check if user has entered the same password in both the boxes
        # on inspecting the password and username elements in the boxes on the form
        # in the browser we learn that the fields are returned as 'username','password1',
        # 'password2'
        try:
            # Here we are using a try except to raise an exception in case of an IntegrityError. First Import
            # integrityError from django.db then use this block. IntegrityError is raised when an exiting username is
            # used again.

            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect ('currentodos')
            else:
                return render(request, "todo/signupuser.html",
                              {"form": UserCreationForm, "error_message": "Passwords do not match",
                               "page_name": "Passwords do not match"})
        except IntegrityError:
            return render(request, "todo/signupuser.html",
                          {"form": UserCreationForm,
                           "error_message": "Username already taken please use another username",
                           "page_name": "Username invalid"})


def loginuser(request):
    pass

def logoutuser(request):
    #checking if the request is post not get. important. browsers tend to preload links so
    #important to set as post not get
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currenttodos(request):
    return render(request, 'todo/currenttodos.html', {'page_name': 'Current Todos'})
