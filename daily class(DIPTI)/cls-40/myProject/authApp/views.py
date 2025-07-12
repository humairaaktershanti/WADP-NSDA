from django.shortcuts import render, redirect
from authApp.models import *
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='logIn')

def home(req):
    if req.user.userType == 'Admin' or req.user.userType == 'Teacher' or req.user.userType =='Student':
        return render(req,'home.html')
    else:
        logout(req)
    return redirect('logIn')

def signUp(req):
    if req.method=='POST':
        username= req.POST.get('username')
        email= req.POST.get('email')
        userType= req.POST.get('userType')
        password= req.POST.get('password')
        password1= req.POST.get('password1')
        if password==password1:
            userr=customUser.objects.create_user(
                username=username,
                email=email,
                userType=userType,
                password=password,
                )
            return redirect('logIn')
           
    return render(req,'signUp.html')


def logIn(req):
    if req.method=='POST':
        username= req.POST.get('username')
        password= req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user:
            login(req, user)
            return redirect('home')
    return render(req,'logIn.html')

def logOut(re):
    logout(re)
    return redirect('logIn')

def addTeacher(req):
    if req.method=='POST':
        username= req.POST.get('username')
        email= req.POST.get('email')
        userType= req.POST.get('userType')
        teacherName= req.POST.get('teacherName')
        phoneNumber= req.POST.get('phoneNumber')        
        profileImage= req.FILES.get('profileImage')

        user = customUser.objects.create_user(
            username=username,
            email=email,
            userType=userType,
            password=phoneNumber,
        )
        teacher = teacherModel(
            user=user,
            teacherName=teacherName,
            phoneNumber=phoneNumber,
            profileImage=profileImage,
        )
        teacher.save()
        return redirect('home')

    return render(req, 'addTeacher.html')

def addStudent(req):
    if req.method=='POST':
        username= req.POST.get('username')
        email= req.POST.get('email')
        userType= req.POST.get('userType')
        studentName= req.POST.get('studentName')
        phoneNumber= req.POST.get('phoneNumber')        
        profileImage= req.FILES.get('profileImage')

        student = studentPendingModel(
            username=username,
            email=email,
            userType=userType,
            studentName=studentName,
            phoneNumber=phoneNumber,
            profileImage=profileImage,
        )
        student.save()
        return redirect('home')
    
    return render(req, 'addStudent.html')

def pendingStudent(req):
    data = studentPendingModel.objects.all()
    context ={
        'data': data
    }
    return render(req, 'pendingStudent.html',context)

def approved(req, id):
    data = studentPendingModel.objects.get(id=id)
    user = customUser.objects.create_user(
        username=data.username,
        email=data.email,
        userType='Student',
        password=data.phoneNumber,
    )
    student = studentModel(
        user=user,
        studentName=data.studentName,
        phoneNumber=data.phoneNumber,
        profileImage=data.profileImage,
    )
    student.save()
    data.delete()
    return redirect('pendingStudent')