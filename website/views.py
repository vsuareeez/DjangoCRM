from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    #Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has iniciado")
            return redirect('home')
        else:
            messages.success(request, 'Error al iniciar, intente de nuevo.')
            return redirect('home')
    else:
        return render (request, 'home.html', {})

#def login_user(request):


def logout_user(request):
    logout(request)
    messages.success(request, 'Has salido.')
    
def register_user(request):
    return render (request, 'register.html', {})