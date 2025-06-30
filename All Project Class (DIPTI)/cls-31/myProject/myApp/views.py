from django.shortcuts import render, redirect
from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(req):
    return render(req,"home.html")


def formTask(req):
    if req.method=='POST':
        
        title=req.POST.get('title')
        description=req.POST.get('description')
        dueDate=req.POST.get('dueDate')
        priority=req.POST.get('priority')
        status=req.POST.get('status')

        data=taskModel(
            title=title,
            description=description,
            dueDate=dueDate,
            priority=priority,
            status=status,
        )
        data.save()
        return redirect ('listTask')
    return render(req,"formTask.html")


def listTask(req):

    data=taskModel.objects.all()
    context={
        'data':data
    }
    return render(req,"listTask.html",context)


def deleteTask(req,id):
    data=taskModel.objects.get(id=id).delete()
    return redirect ('listTask')


def viewsTask(req,id):
    data=taskModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,"viewsTask.html",context)


def editTask(req,id):
    data=taskModel.objects.get(id=id)
    context={
        'data':data
    }

    if req.method=='POST':
        data.id=id
        data.title=req.POST.get('title')
        data.description=req.POST.get('description')
        data.dueDate=req.POST.get('dueDate')
        data.priority=req.POST.get('priority')
        data.status=req.POST.get('status')


        data.save()
        return redirect ('listTask')

    return render(req,"editTask.html",context)



    
def signUp(req):
    if req.method=='POST':
        username=req.POST.get('username')
        email=req.POST.get('email')
        password=req.POST.get('password')
        confirmPassword=req.POST.get('confirmPassword')
        profilePhoto=req.POST.get('profilePhoto')
        bio=req.POST.get('bio')

        if password==confirmPassword:
            customerModel.objects.create_user(
                username=username,
                email=email,
                password=confirmPassword,
                profilePhoto=profilePhoto,
                bio=bio,
            )

            return redirect('signIn')
        return render(req,"signUp.html")
    

def signIn(req):
    if req.method=='POST': 
           username=req.POST.get('username')
           password=req.POST.get('password')

           user=authenticate(req,username=username, password=password)
           if user:
               login(req, user)
               return redirect('home')
    return render(req,'signIn.html')
    


def logOut(req):
    logout(req)
    return redirect ('signIn')    
    


    