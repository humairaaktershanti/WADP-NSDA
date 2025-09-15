from django.shortcuts import render,redirect
from myapp.models import *


def signUp(req):

    if req.method=='POST':
        username=req.POST.get('username')
        first_name=req.POST.get('first_name')
        last_name=req.POST.get('first_last_namename')
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
                password=password,
                confirm_password=confirm_password,
                bio=bio,
                image=image,
                address=address,
                userType=userType
            )
            data.save()
            return redirect('logIn')
    return render(req,'signUp.html')


def logIn(req):
    if req.method=='POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        data=customUserModel(
                username=username,
                password=password,
        )
        data.save()
    return redirect('home')
