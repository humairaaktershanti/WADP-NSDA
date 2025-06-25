from django.shortcuts import render,redirect
from myApp.models import *
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def signUp(req):

    if req.method=='POST':
        username=req.POST.get("username")
        fullName=req.POST.get('fullName')
        email=req.POST.get("email")
        mobileNumber=req.POST.get("mobileNumber")
        gender=req.POST.get("gender")
        age=req.POST.get("age")
        dateOfBirth=req.POST.get("dateOfBirth")
        presentAddress=req.POST.get("presentAddress")
        permanentAddress=req.POST.get("permanentAddress")
        lastEducationName=req.POST.get("lastEducationName")
        instutiteName=req.POST.get("instutiteName")
        passingYear=req.POST.get("passingYear")
        grade=req.POST.get("grade")
        if req.FILES.get("profileimage"):
            profileimage=req.FILES.get("profileimage")
        password=req.POST.get("password")

        user=customUser.objects.create_user(
            username=username,
            fullName=fullName,
            email=email,
            mobileNumber=mobileNumber,
            gender=gender,
            age=age,
            dateOfBirth=dateOfBirth,
            presentAddress=presentAddress,
            permanentAddress=permanentAddress,
            lastEducationName=lastEducationName,
            instutiteName=instutiteName,
            passingYear=passingYear,
            grade=grade,
            profileimage=profileimage,
            password=password,
        )
    
        return redirect("signIn")
    return render (req,'signUp.html')


def signIn(req):
    if req.method=='POST':
        username=req.POST.get("username")
        password=req.POST.get("password")
        user= authenticate(req, username=username, password=password)
        if user:
            login(req,user)
            return redirect("home")
 
    return render (req,'signIn.html')

def home(req):
    return render(req,'home.html')

def logOut(req):
    logout(req)


    return redirect('signIn')



    