from django.shortcuts import render,redirect
from myApp.models import *
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def signUp(req):

    if req.method=='POST':
        username=req.POST.get("username")
        email=req.POST.get("email")
        password=req.POST.get("password")
        confirm_password=req.POST.get("confirm_password")
        role=req.POST.get("role")

        if password==confirm_password:

            user=customUser.objects.create_user(
                username=username,
                email=email,
                password=confirm_password,
                user_type=role,
            )
            return redirect("signIn")
    return render (req,'signUp.html')


def signIn(req):
    if req.method=='POST':
        username=req.POST.get("username")
        password=req.POST.get("password")
        user= authenticate(req, username=username, password=password)
        if user:
            login(req,user)
            return redirect("home")
 
    return render (req,'signIn.html')

def home(req):
    return render(req,'home.html')

def logOut(req):
    logout(req)


    return redirect('signIn')
    