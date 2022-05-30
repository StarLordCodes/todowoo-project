from django.shortcuts import render


def home(request):
    return render(request, "todo/home.html", {"page_name": "Home page"})


def signupuser(request):
    pass


def loginuser(request):
    pass
