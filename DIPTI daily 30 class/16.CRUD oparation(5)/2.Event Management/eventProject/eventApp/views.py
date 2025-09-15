from django.shortcuts import render,redirect
from eventApp.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required



@login_required(login_url='logIn')
def home(req):
    return render(req,"home.html")

@login_required(login_url='logIn')
def addEvent(req):
    if req.method == 'POST':
        user=req.user
        title=req.POST.get('title')
        date=req.POST.get('date')
        location=req.POST.get('location')
        description=req.POST.get('description')
        image=req.POST.get('image')

        data=eventModel(
            user=user,
            title=title,
            date=date,
            location=location,
            description=description,
            image=image,
        )
        data.save()
        return redirect('listEvent')

    return render(req,"addEvent.html")

@login_required(login_url='logIn')
def listEvent(req):
    data=eventModel.objects.filter(user=req.user)
    adminData=eventModel.objects.all()
    context={
        'data':data,
        'adminData':adminData,
    }
    return render(req,"listEvent.html",context)

@login_required(login_url='logIn')
def veiwEvent(req,id):
    data=eventModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,"veiwEvent.html",context)

@login_required(login_url='logIn')
def deleteEvent(req,id):
    data=eventModel.objects.get(id=id).delete()
    return redirect ('listEvent')

@login_required(login_url='logIn')
def editEvent(req,id):
    data=eventModel.objects.get(id=id)
    context={
        'data':data
    }

    if req.method == 'POST':
        data.id=id
        data.title=req.POST.get('title')
        data.date=req.POST.get('date')
        data.location=req.POST.get('location')
        data.description=req.POST.get('description')
        if req.POST.get('image'):
          data.image=req.POST.get('image')


        data.save()
        return redirect('listEvent')
    return render(req,"editEvent.html",context)


def signUp(req):
    if req.method=='POST':
        username=req.POST.get('username')
        userType=req.POST.get('userType')
        password=req.POST.get('password')
        password1=req.POST.get('password1')

        if password==password1:

            data=customUserModel(
                username=username,
                userType=userType,
                password=make_password(password),

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

@login_required(login_url='logIn')
def logOut(req):
    logout(req)
    return redirect('logIn')       

@login_required(login_url='logIn')
def changepass(req):
    currentUser=req.user
    if req.method=='POST':
          oldPassword=req.POST.get('oldPassword')
          newPassword=req.POST.get('newPassword')
          confirmPassword=req.POST.get('confirmPassword')
          if check_password(oldPassword,req.user.password):
              if newPassword==confirmPassword:
                  currentUser.set_password(newPassword)
          currentUser.save()
          return redirect('logIn')
    return render(req,'changepass.html')
              
                  





          


