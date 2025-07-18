from django.shortcuts import render,redirect
from portalApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            userType='Admin',
            )

        return redirect('logIn')
    return render(request, 'signUp.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  

    return render(request, 'logIn.html')

def logOut(request):
    logout(request)
    return redirect('logIn')

def home(request):
    return render(request, 'home.html')

    