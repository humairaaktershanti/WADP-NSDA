from django.shortcuts import render, redirect
from toDoApp.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


def signUp(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        fullName = req.POST.get('fullName')
        email = req.POST.get('email')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')
        image = req.FILES.get('image')
        address = req.POST.get('address')
        citynName = req.POST.get('citynName')
        bio = req.POST.get('bio')
        phone = req.POST.get('phone')

        if password == confirm_password:
            data = customUser(
                username = username,
                fullName=fullName,
                email=email,
                password=password,
                image=image,
                address=address,
                citynName=citynName,
                bio=bio,
                phone=phone,
            )
            data.save()

            return redirect('logIn')
    return render(req, 'signUp.html')

def logIn(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user= authenticate(req,username=username,password=password)
        if user:
            login(req,user)
            return redirect("updatePassword")
        
    return render(req, 'logIn.html')

def logOut(req):
    logout(req)

    return redirect('logIn')

def updatePassword(req):
    user = req.user
    if req.method == 'POST':
        oldPassword = req.POST.get('oldPassword')
        newPassword = req.POST.get('newPassword')
        confurmPassword = req.POST.get('confurmPassword')

        if check_password(oldPassword, req.user.password):
            if newPassword == confurmPassword:
                user.set_password(newPassword)
                user.save()

            return redirect('index')
    return render(req, 'updatePassword.html')