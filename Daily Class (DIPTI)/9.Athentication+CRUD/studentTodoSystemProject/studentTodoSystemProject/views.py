from django.shortcuts import render, redirect
from studentApp.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



@login_required(login_url="/Login/")
def home(req):
    return render(req,"home.html")

@login_required(login_url="/Login/")
def addStudent(req):
    if req.method=='POST':
        name=req.POST.get('name')
        roll_no=req.POST.get('roll_no')
        department=req.POST.get('department')
        student_image=req.FILES.get('student_image')

        data=studentModel(
            name=name,
            roll_no=roll_no,
            department=department,
            student_image=student_image

        )

        data.save()

        return redirect('studentList')

    return render(req,"addStudent.html")


@login_required(login_url="/Login/")
def studentList(req):
    data=studentModel.objects.all()
    context={
        'data': data
    }
    return render(req,"studentList.html",context)

@login_required(login_url="/Login/")
def viewStudent(req,id):
    data=studentModel.objects.get(id=id)
    context={
        'data':data
    }

    return render (req,"viewStudent.html",context)

@login_required(login_url="/Login/")
def deleteStudent(req,id):
    data=studentModel.objects.get(id=id).delete()

    return redirect ('studentList')

@login_required(login_url="/Login/")
def editStudent(req,id):
    data=studentModel.objects.get(id=id)
    context={
        'data':data
    }
    if req.method=='POST':
        data.id=id
        data.name=req.POST.get('name')
        data.roll_no=req.POST.get('roll_no')
        data.department=req.POST.get('department')
        if req.FILES.get('student_image'):

            data.student_image=req.FILES.get('student_image')

        data.save()

        return redirect('studentList')

    
    return render (req,"editStudent.html",context)







@login_required(login_url="/Login/")
def addTask(req):
    if req.method=='POST':
        title=req.POST.get('title')
        description=req.POST.get('description')
        status=req.POST.get('status')
        due_date=req.POST.get('due_date')

        data=toDoModel(
            title=title,
            description=description,
            status=status,
            due_date=due_date,


        )
        data.save()

        return redirect('taskList')

    return render(req,"addTask.html")

@login_required(login_url="/Login/")
def taskList(req):
    data=toDoModel.objects.all()
    context={
        'data': data
    }
    return render(req,"taskList.html",context)


@login_required(login_url="/Login/")
def viewTask(req,id):
    data=toDoModel.objects.get(id=id)
    context={
        'data':data
    }

    return render (req,"viewTask.html",context)

@login_required(login_url="/Login/")
def deleteTask(req,id):

    data=toDoModel.objects.get(id=id).delete()

    return redirect ('taskList')


@login_required(login_url="/Login/")
def editTask(req,id):
    data=toDoModel.objects.get(id=id)
    context={
        
        'data':data
    }
    if req.method=='POST':
        data.id=id
        data.title=req.POST.get('title')
        data.description=req.POST.get('description')
        data.status=req.POST.get('status')
        data.due_date=req.POST.get('due_date')

        data.save()

        return redirect('taskList')
    
    return render (req,"editTask.html",context)









def SignUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password1')
        confirm_password = req.POST.get('password2')
        
        if password == confirm_password:
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('Login')
    return render(req, 'signUp.html')

def Login(req):
    if req.method=='POST':
        Username = req.POST.get('username')
        Password = req.POST.get('password')
        
        user = authenticate(req, username=Username, password=Password)
        
        if user is not None:
            login(req, user)
            return redirect('home')
        
    return render(req, 'logIn.html')

def logOut(req):
    logout(req)
    return redirect('home')