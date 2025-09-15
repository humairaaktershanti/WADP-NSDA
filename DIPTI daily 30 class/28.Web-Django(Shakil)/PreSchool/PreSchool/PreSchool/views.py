from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from PreSchoolApp.models import *

def signupPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        
        if password == confirmpassword:
            user = customeUser.objects.create_user(username=username, password=password)
            user.email = email
            user.UserType = '1'
            user.save()
            return redirect('signinPage')
        else:
            return redirect('signupPage')

    return render(request,'commons/signup.html')

def signinPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        if user:
            print("User type: ",user.UserType)
            if user.UserType == '1':
                login(request,user)
                return redirect('adminDashboard')
            
            elif user.UserType == '2':
                login(request,user)
                return redirect('studentDashboard')
            
            elif user.UserType == '3':
                login(request,user)
                return redirect('studentDashboard')
    
    return render(request,'commons/signin.html')

def logoutPage(request):
    logout(request)
    return redirect('signinPage')

#-----------Admin Section--------------------

@login_required
def adminDashboard(request):
    
    return render(request,'myadmin/admindashboard.html')
