from django.shortcuts import render,redirect
from myApp.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# @login_required(login_url='logIn')
def home(req):
    return render(req,'home.html')

def signUp(req):
    if req.method == 'POST':
        username=req.POST.get('username')
        userType=req.POST.get('userType')
        password=req.POST.get('password')
        password1=req.POST.get('password1')

        if password==password1:
            data=customUserModel(
                username=username,
                userType=userType,
                password=make_password(password)
            )
            data.save()
            return redirect('logIn')

    return render(req,'signUp.html')

def logIn(req):
    if req.method == 'POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        user=authenticate(req,username=username,password=password)
        if user:
            login(req,user)
            return redirect('home')
    return render(req,'logIn.html')
    

def logOut(req):
    logout(req)
    return redirect('logIn')


def changePassword(req):
    currentUser=req.user
    if req.method == 'POST':
        newPassword=req.POST.get('newPassword')
        oldPassword=req.POST.get('oldPassword')
        confirmPassword=req.POST.get('confirmPassword')
        if check_password(oldPassword,req.user.password):
            if newPassword==confirmPassword:
                currentUser.set_password(newPassword)
                currentUser.save()
                return redirect('logIn')
    return render(req,'changePassword.html')
             
                  



     
