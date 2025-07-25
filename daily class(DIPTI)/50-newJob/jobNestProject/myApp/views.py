from django.shortcuts import render, redirect


from django.contrib.auth import authenticate, login, logout
from myApp.models import *
from django.contrib.auth.decorators import login_required 

def index(req):
    return render(req,'index.html')

def register(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        userType = req.POST.get('userType')
        password = req.POST.get('password')
        confirmPassword = req.POST.get('confirmPassword')
        
        
        if password == confirmPassword:
            user = customUserModel.objects.create_user(
                username = username,
                email = email,
                password = password,
                userType = userType, 
                )
            return redirect('login')
    return render(req, 'register.html')

def logIn(req):
    if req.method=='POST':
        Username = req.POST.get('username')
        Password = req.POST.get('password')
        
        user = authenticate(req, username=Username, password=Password)
        
        if user is not None:
            login(req,user)
            data = customUserModel.objects.filter(user=Username)
            if data.userType == 'recruiters':
                return redirect('dashboard_recruiter')
            else:
                return redirect('dashboard_seeker')
        
    return render(req, 'login.html')

@login_required(login_url='login')
def logOut(req):
    logout(req)
    return redirect('login')


@login_required(login_url='login')
def change_password(req):
    if req.method=='POST':
        oldPassword = req.POST.get('oldPassword')
        newPassword = req.POST.get('newPassword')
        confirmPassword = req.POST.get('confirmPassword')
        if newPassword == confirmPassword:
            if req.user.check_password(oldPassword):
                req.user.set_password(newPassword)
                req.user.save()
                logout(req)
                return redirect('login')
    return render(req, 'change_password.html')