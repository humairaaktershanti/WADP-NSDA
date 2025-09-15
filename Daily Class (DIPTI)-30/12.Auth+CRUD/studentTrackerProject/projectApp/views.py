from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import customUserModel
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def logIn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "logIn.html")

def signUp(request):
    newUser = customUserModel()
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")
        studentName = request.POST.get("studentName")
        studentId = request.user.id 

        if password == confirmPassword:
            newUser.username = username
            newUser.email = email
            newUser.set_password(password)
            newUser.studentName = studentName
            newUser.studentId = studentId

            newUser.save()
            messages.success(request, "Account created successfully.")
            return redirect("logIn")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "signUp.html")

def logOut(request):
    logout(request)
    return redirect("logIn")

@login_required(login_url='logIn')
def index(request):
    return render(request, "index.html")

@login_required(login_url='logIn')
def projectList(req):
    data = projectModel.objects.all()
    context ={
        'data' : data
    }
    return render(req, 'projectList.html', context)

@login_required(login_url='logIn')
def delete(req, id):
    data = projectModel.objects.get(id=id).delete()
    return redirect('projectList')

@login_required(login_url='logIn')
def view(req, id):
    data = projectModel.objects.get(id=id)
    context ={
        'data' : data
    }
    return render(req, 'view.html', context)

@login_required(login_url='logIn')
def edit(req, id):
    data = projectModel.objects.get(id=id)
    context ={
        'data' : data
    }
    if req.method == 'POST':
        data.projectName = req.POST.get('projectName')
        data.projectDescription = req.POST.get('projectDescription')
        data.projectStatus = req.POST.get('projectStatus')
        data.createdBy = req.user.studentName
        data.save()
        return redirect('projectList')
    return render(req, 'edit.html', context)

@login_required(login_url='logIn')
def addProject(req):

    if req.method == 'POST':
        projectName = req.POST.get('projectName')
        projectDescription = req.POST.get('projectDescription')
        projectStatus = req.POST.get('projectStatus')
        createdBy = req.user.studentName

        newProject = projectModel(
            projectName = projectName,
            projectDescription = projectDescription,
            projectStatus = projectStatus,
            createdBy = createdBy
        )
        newProject.save()
        return redirect('projectList')
    return render(req, 'addProject.html')
