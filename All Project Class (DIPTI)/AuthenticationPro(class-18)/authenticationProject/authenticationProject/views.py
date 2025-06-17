from django.shortcuts import render
from user_authApp.models import *
fromdjango.contrib.auth


def registration(req):
    if req.method =='POST':
        fullName=req.POST.get('fullName')
        username1=req.POST.get('username1')
        name=req.POST.get('name')
        username2=req.POST.get('username2')
        email=req.POST.get('email')
        contact=req.POST.get('contact')
        password=req.POST.get('password')
        confirmPassword=req.POST.get('confirmPassword')
        if password == confirmPassword:
            userinfo = UserAuthModel.objects.create(
            username=username1,
            full_name=fullName,
            email=email,
            contact_number=contact,
            password=password
            )    

            
            userinfo.save()
            return redirect('login')
        else:
            print("password dont match")
    return render(req,'registration.html')

def login(req):
    return render(req,'logIn.html')


def home(req):
    return render(req,'home.html')


