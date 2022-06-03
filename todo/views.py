from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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

@login_required
def logoutuser(request):
    # checking if the request is post not get. important. browsers tend to preload links so
    # important to set as post not get
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    # if you use todos = Todo.objects.all() we get the objects of all the users
    # we only want the todos of the current user, also checking if datecompleted is null
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'page_name': 'Current Todos', 'todos': todos})

@login_required
# last function created , to see all the completed todos extremely similar to currenttodos
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'todo/completedtodos.html', {'todos': todos, 'page_name': 'Completed Todos'})


@login_required
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


@login_required
def viewtodo(request, todo_pk):
    # todo = get_object_or_404(Todo,pk=todo_pk) this allows access to all users so we have to change it to show only
    # objects of the current user or else show 404 so we add user = request.user too.
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        # if get method then show the contents of the "todoform". It is easy in django to show the form for the current
        # object. You just have to pass the object into the form as argument like here. Then pass the form onto the html
        # view.
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'form': form, 'todo': todo})
    else:
        # again use try except for handling errors
        try:
            # take the changed value if the user makes any change and pass it onto the "TodoForm" and then save it for
            # the instant todo which we got at the beginning of the function
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {"error_message": "Bad data. Try again",
                                                          "form": form, "todo": todo})


@login_required
def completetodo(request, todo_pk):
    # getting the required object only
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    # getting the required object only
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

