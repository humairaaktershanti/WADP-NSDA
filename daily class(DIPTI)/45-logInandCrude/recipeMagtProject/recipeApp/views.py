from django.shortcuts import render,redirect
from recipeApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="logIn")
def home(req):
    return render(req,'home.html')

def signUp(req):
    if req.method=="POST":
        username=req.POST.get('username')
        email=req.POST.get('email')
        password=req.POST.get('password')
        password1=req.POST.get('password1')

        if password==password1:

            data=User.objects.create_user(
                username=username,
                email=email,
                password=password1,             
            )
            return redirect('logIn')
    return render(req,'signUp.html')

def logIn(req):
    if req.method=="POST":
        username=req.POST.get('username')
        password=req.POST.get('password')

        user=authenticate(req,username=username,password=password)
        if user:
            login(req,user)
            return redirect('home')
    return render(req,'logIn.html')

@login_required(login_url="logIn")
def logOUT(req):
    logout(req)
    return redirect('logIn')


@login_required(login_url='logIn')
def Addrecipe(req):
    if req.method=='POST':
        name=req.POST.get('name')
        creator=req.POST.get('creator')
        description=req.POST.get('description')
        ingredients=req.POST.get('ingredients')
        instructions=req.POST.get('instructions')
        image=req.FILES.get('image')
        data=recipeModel(
            name=name,
            creator=creator,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            image=image,
        )
        data.save()
        return redirect('listRecipe')
    return render(req,'Addrecipe.html')

@login_required(login_url='logIn')
def listRecipe(req):
    data=recipeModel.objects.all()
    context={
        'data':data
    }
    return render(req,'listRecipe.html',context)

@login_required(login_url='logIn')
def deleteRecipe(req,id):
    data=recipeModel.objects.get(id=id).delete()

    return redirect('listRecipe')

@login_required(login_url='logIn')
def editRecipe(req,id):
    data=recipeModel.objects.get(id=id)
    context={
        'data':data
    }

    if req.method=='POST':
        data.name=req.POST.get('name')
        data.creator=req.POST.get('creator')
        data.description=req.POST.get('description')
        data.ingredients=req.POST.get('ingredients')
        data.instructions=req.POST.get('instructions')
        
        if req.FILES.get('image'):
            data.image=req.FILES.get('image')

        data.save()
        return redirect('listRecipe')
    
    return render(req,'editRecipe.html',context)

@login_required(login_url='logIn')
def viewRecipe(req,id):
    data=recipeModel.objects.get(id=id)
    context={
        'i':data
    }
    return render(req,'viewRecipe.html',context)

    