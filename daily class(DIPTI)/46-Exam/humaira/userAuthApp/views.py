from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

# for Authenticaton
from django.contrib.auth import authenticate, login, logout
from userAuthApp.models import *
from django.contrib.auth.decorators import login_required 

@login_required(login_url='logIn')
def home(req):
    return render(req, 'home.html')

def signUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        userTypes = req.POST.get('userTypes')

        phone = req.POST.get('phone')

        if userTypes=='Admin':

            user = customUserModel.objects.create_user(
                username = username,
                email = email,
                password = phone,
                userTypes = userTypes, 
                )
            return redirect('logIn')
        else:
            user = pendingAccountModel(
                username = username,
                email = email,
                userTypes = userTypes, 
                )
            user.save()
            return redirect('logIn')
        
    return render(req, 'signUp.html')

def logIn(req):
    if req.method=='POST':
        Username = req.POST.get('username')
        Password = req.POST.get('password')
        
        user = authenticate(req, username=Username, password=Password)
        
        if user is not None:
            login(req, user)
            return redirect('home')
        
    return render(req, 'logIn.html')

@login_required(login_url='logIn')
def logOut(req):
    logout(req)
    return redirect('logIn')


@login_required(login_url='logIn')
def changePassword(req):
    if req.method=='POST':
        oldPassword = req.POST.get('oldPassword')
        newPassword = req.POST.get('newPassword')
        confirmPassword = req.POST.get('confirmPassword')
        if newPassword == confirmPassword:
            if req.user.check_password(oldPassword):
                req.user.set_password(newPassword)
                req.user.save()
                logout(req)
                return redirect('logIn')
    return render(req, 'changePassword.html')