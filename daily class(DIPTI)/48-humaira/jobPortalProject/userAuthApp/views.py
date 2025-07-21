
from django.shortcuts import render, redirect
from userAuthApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from employerApp.models import *
from candidateApp.models import*

def home(req):
    return render(req, 'home.html')

def signUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        userTypes = req.POST.get('userTypes')      

        if userTypes=='Admin':
            customUserModel.objects.create_user(
                username = username,
                email = email,
                phone=phone,               
                userTypes = userTypes, 
                password = phone,                
                )
            return redirect('logIn')
        else:
            pendingAccountModel.objects.create(
                username = username,
                email = email,
                phone=phone,               
                userTypes = userTypes, 
                pendingStatus='Pending',
                )
            return redirect('logIn')
                
    return render(req, 'signUp.html')

def logIn(req):
    if req.method=='POST':
        Username = req.POST.get('username')
        Password = req.POST.get('password')
        
        user = authenticate(req, username=Username, password=Password)
        
        if user:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req,'User does not exists.')
            return redirect('logIn')
          
    return render(req, 'logIn.html')

def logOut(req):
    logout(req)
    return redirect('logIn')

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

def pendingList(req):
    data=pendingAccountModel.objects.all()
    context={
        'data':data
    }

    return render(req,'pendingList.html',context)

def acceptPending(req,id):
    data=pendingAccountModel.objects.get(id=id)
    if data:
        user = customUserModel.objects.create_user(
            username = data.username,
            email = data.email,
            phone = data.phone,               
            userTypes = data.userTypes, 
            password = str(data.phone),          
            
        )
        if user:
            if data.userTypes == 'Employer':
                employerProfileModel.objects.create(
                    employerUser = user,
                    email = data.email,
                    phone=data.phone,               

                )
            elif data.userTypes == 'Candidate':
                candidateProfileModel.objects.create(
                    candidateUser = user,
                    email = data.email,
                    phone=data.phone,            

                )
        data.delete()        
        return redirect('pendingList')