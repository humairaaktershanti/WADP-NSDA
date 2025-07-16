from django.shortcuts import render
from authApp.models import *
# Create your views here.

def home(req):
    return render(req,'home.html')

def signUp(req):
    if req.method=='POST':
        username= req.POST.get('username')
        email= req.POST.get('email')
        userType= req.POST.get('userType')
        password= req.POST.get('password')
        password1= req.POST.get('password1')
        if password==password1:
            data=customUser.objects.create_user(
                username=username,
                email=email,
                userType=userType,
                password=password,
                )
            data.save()
            return render(req,'logIn.html')
           
    return render(req,'signUp.html')

def logIn(req):
    return render(req,'logIn.html')