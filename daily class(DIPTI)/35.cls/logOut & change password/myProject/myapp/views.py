from django.shortcuts import render,redirect
from myapp.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required

@login_required
def home(req):
    return render(req,'home.html')


def signUp(req):

    if req.method=='POST':
        username=req.POST.get('username')
        first_name=req.POST.get('first_name')
        last_name=req.POST.get('last_name')
        email=req.POST.get('email')
        password=req.POST.get('password')
        confirm_password=req.POST.get('confirm_password')
        bio=req.POST.get('bio')
        image=req.POST.get('image')
        address=req.POST.get('address')
        userType=req.POST.get('userType')

        if password==confirm_password:

            data=customUserModel(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                bio=bio,
                image=image,
                address=address,
                userType=userType,
            )
            data.save()
            return redirect('logIn')
    return render(req,'signUp.html')


def logIn(req):
    if req.method=='POST':
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
    current_user=req.user
    if req.method=='POST':
        oldPassword=req.POST.get('oldPassword')
        newPassword=req.POST.get('newPassword')
        confirmPassword=req.POST.get('confirmPassword')

        if check_password(oldPassword, req.user.password):
            if newPassword == confirmPassword:
                    current_user.set_password(newPassword)
                    current_user.save()
                    return redirect('logIn')
    return render(req,'changePassword.html')



 
