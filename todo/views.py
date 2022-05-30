from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, "todo/home.html", {"page_name": "Home page"})


def signupuser(request):
    return render(request, "todo/signupuser.html", {"form": UserCreationForm, "page_name": "Signup page"})


def loginuser(request):
    pass
