from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth import authenticate, login, logout
from authApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='logIn')
def index(req):
    return render(req, 'index.html')

def signUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        userTypes = req.POST.get('userTypes')

        usernameis = customUserModel.objects.get(username=username)
        if usernameis:
            messages.error(req, 'Username already exists')
            return render(req, 'signUp.html')
        
        if userTypes == 'Admin':
            user = customUserModel.objects.create_user(
                username = username,
                email = email,
                phone = phone,
                password = phone,
                userTypes = userTypes,
                )
            return redirect('logIn')
        else:
            user = pendingAccountModel(
                username = username,
                email = email,
                phone = phone,
                userTypes = userTypes,
                pendingStatus = 'Pending'
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
            return redirect('index')
        
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
    return render(req, 'user_auth/changePassword.html')

@login_required(login_url='logIn')
def pendingAccount(req):
    data = pendingAccountModel.objects.all()
    context={
        'data':data
    }
    return render(req, 'pendingAccount.html', context)

@login_required(login_url='logIn')
def accept(req, id):
    data = pendingAccountModel.objects.get(id=id)

    user = customUserModel.objects.create_user(
        username = data.username,
        email = data.email,
        phone = data.phone,
        password = str(data.phone),
        userTypes = data.userTypes
        )
    user.save()
    
    data = pendingAccountModel.objects.get(id=id).delete()
    return redirect("pendingAccount")

@login_required(login_url='logIn')
def deny(req, id):
    data = pendingAccountModel.objects.get(id=id).delete()
    return redirect("pendingAccount")