from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm


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
                return redirect('currentodos')
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
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {"form": AuthenticationForm})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {"form": UserCreationForm,
                                                           "error_message": "Incorrect password username combination"})
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    # checking if the request is post not get. important. browsers tend to preload links so
    # important to set as post not get
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    return render(request, 'todo/currenttodos.html', {'page_name': 'Current Todos'})


def createtodo(request):
    # In case of get, just provide a form to create the todo object
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm})
    else:
        # In case of an error we might want to print an error message. The error is unlikely
        # but we have to be prepared
        try:
            form = TodoForm(request.POST)
            # Now save the form without committing it to database
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm,
                                                            'error_message': 'Bad data. Please try again'})
