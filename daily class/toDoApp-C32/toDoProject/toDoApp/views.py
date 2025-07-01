from django.shortcuts import render, redirect
from toDoApp.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


def signUp(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        fullName = req.POST.get('fullName')
        email = req.POST.get('email')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')
        image = req.FILES.get('image')
        address = req.POST.get('address')
        citynName = req.POST.get('citynName')
        bio = req.POST.get('bio')
        phone = req.POST.get('phone')

        if password == confirm_password:
            data = customUser.objects.create_user(
                username = username,
                fullName=fullName,
                email=email,
                password=password,
                image=image,
                address=address,
                citynName=citynName,
                bio=bio,
                phone=phone,
            )
            data.save()

            return redirect('logIn')
    return render(req, 'signUp.html')

def logIn(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user= authenticate(req,username=username,password=password)
        if user:
            login(req,user)
            return redirect("index")
        
    return render(req, 'logIn.html')

def logOut(req):
    logout(req)
    return redirect('logIn')

def updatePassword(req,id):
    user = req.user
    if req.method == 'POST':
        oldPassword = req.POST.get('oldPassword')
        newPassword = req.POST.get('newPassword')
        confurmPassword = req.POST.get('confurmPassword')

        if check_password(oldPassword, req.user.password):
            if newPassword == confurmPassword:
                user.set_password(newPassword)
                user.save()

            return redirect('index')
    return render(req, 'updatePassword.html')


def index(req):
    data = toDoModel.objects.filter(user=req.user)
    statusVariable1=toDoModel.objects.filter(user=req.user,status='pending')
    statusVariable2=toDoModel.objects.filter(user=req.user,status='inProgress')
    statusVariable3=toDoModel.objects.filter(user=req.user,status='completed')

    context={
        'data':data, 
        'statusVariable1':statusVariable1,
        'statusVariable2':statusVariable2,
        'statusVariable3':statusVariable3,
         
    }
    return render (req,'index.html',context)


def addToDo(req):

    if req.method=='POST':
        
        title=req.POST.get('title')
        description=req.POST.get('description')
        status=req.POST.get('status')
        created_at=req.POST.get('created_at')
        updated_at=req.POST.get('updated_at')

        data=toDoModel(
            title=title,
            description=description,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )
        data.save()
        return redirect ('listToDo')
    return render(req,"addToDo.html")


def listToDo(req):

    data= toDoModel.objects.filter(user=req.user)
    
    context={
        'data':data
        
    }
    return render(req,"listToDo.html",context)





def deleteToDo(req,id):
    data=toDoModel.objects.get(id=id).delete()
    return redirect ('listToDo')


def viewsToDo(req,id):
    data=toDoModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,"viewsToDo.html",context)


def editToDo(req,id):
    data=toDoModel.objects.get(id=id)
    context={
        'data':data
    }

    if req.method=='POST':
        data.id=id
        data.title=req.POST.get('title')
        data.description=req.POST.get('description')
        data.status=req.POST.get('status')
        data.created_at=req.POST.get('created_at')
        data.updated_at=req.POST.get('updated_at')


        data.save()
        return redirect ('listToDo')

    return render(req,"editToDo.html",context)


def DoneToDo(req,id):
    data=toDoModel.objects.get(id=id)
    data.status='Completed'
    data.save()
    return redirect('listToDo')


    