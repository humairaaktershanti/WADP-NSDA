from django.shortcuts import render

# Create your views here.
from myApp.views import *

def signUp(req):
    if req.method == 'POST':
     fullName=req.POST.get('fullName')
    bio=req.POST.get('bio')
    userType=req.POST.get('userType')
    username=req.POST.get('username')
    password1=req.POST.get('password1')
    password2=req.POST.get('password2')

    data=cu
    if password1==password2:
       data=customUserModel(
       fullName=fullName,
       bio=bio,
       userType=userType,
       username=username,
       password=password1,



