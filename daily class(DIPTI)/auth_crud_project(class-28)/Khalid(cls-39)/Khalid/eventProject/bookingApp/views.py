from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from bookingApp.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def Register(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password1 = req.POST.get('password1')
        password2 = req.POST.get('password2')
        fullName = req.POST.get('fullName')
        phoneNumber = req.POST.get('phoneNumber')
        profileImg = req.FILES.get('profileImg')

        if password1==password2:
            newUser = eventUserModel(
                username=username,
                email=email,
                fullName=fullName,
                phoneNumber=phoneNumber,
                profileImage=profileImg,
            )
            newUser.set_password(password1)
            newUser.save()
            return redirect('logIn')
    return render(req, 'Register.html')

def logIn(req):
    if req.method=='POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user:
            print(user)
            login(req, user)
            return redirect('index')
    return render(req, 'logIn.html')

@login_required(login_url='logIn')
def logOut(req):
    logout(req)
    return redirect('logIn')

@login_required(login_url='logIn')
def index(req):
    data = eventBookingModel.objects.all()
    context={
        'data': data
    }
    return render(req, 'index.html',context)

@login_required(login_url='logIn')
def profile(req):
    return render(req, 'profile.html')

@login_required(login_url='logIn')
def addBooking(req):
    if req.method=='POST':
        eventTitle = req.POST.get('eventTitle')
        eventType = req.POST.get('eventType')
        eventDescription = req.POST.get('eventDescription')
        eventDate = req.POST.get('eventDate')
        # status = req.POST.get('status')
        location = req.POST.get('location')

        add = eventBookingModel(
            eventTitle = eventTitle,
            eventType = eventType,
            eventDescription = eventDescription,
            eventDate = eventDate,
            status = 'NotStart',
            location = location,
            createdBy = req.user.fullName
        )
        add.save()
        return redirect('myBooking')
    return render(req, 'addBooking.html')

@login_required(login_url='logIn')
def myBooking(req):
    data = eventBookingModel.objects.all()
    context = {
        'data': data
    }
    return render(req, 'myBooking.html', context)

@login_required(login_url='logIn')
def update(req, id):
    data = eventBookingModel.objects.get(id=id)
    if data.status == 'NotStart':
        data.status = 'InProgress'
    elif data.status == 'InProgress':
        data.status = 'Completed'
    data.save()
    return redirect('myBooking')

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
    return render(req, 'changePassword.html')

@login_required(login_url='logIn')
def delete(req, id):
    data = eventBookingModel.objects.get(id=id)
    data.delete()
    return redirect('myBooking')