from django.shortcuts import render, redirect
from auth_crud_app.models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(req):
    return render(req,"home.html")


def addProduct(req):
    if req.method=='POST':
        productName=req.POST.get('productName')
        productDescription=req.POST.get('productDescription')
        productPrice=req.POST.get('productPrice')
        productImage=req.FILES.get('productImage')
        created_at=req.POST.get('created_at')

        data=productModel(
            productName=productName,
            productDescription=productDescription,
            productPrice=productPrice,
            productImage=productImage,
            created_at=created_at,

        )
        data.save()
        return redirect ("listProduct")
    
    return render(req,'addProduct.html')


def listProduct(req):
    data=productModel.objects.all()
    context={
        'data': data
    }
    return render(req,'listProduct.html',context)


def viewProduct(req,id):
    data=productModel.objects.get(id=id)

    context={
        'data': data
    }
    return render (req,"viewProduct.html", context)

def deleteProduct(req,id):
    data=productModel.objects.get(id=id).delete()
    return redirect('listProduct')

def editProduct(req,id):
    data=productModel.objects.get(id=id)

    context={
        'data': data
    }

    if req.method=='POST':
        data.id=id
        data.productName=req.POST.get('productName')
        data.productDescription=req.POST.get('productDescription')
        data.productPrice=req.POST.get('productPrice')


        if req.FILES.get('productImage'):
             data.productImage=req.FILES.get('productImage')

        data.created_at=req.POST.get('created_at')

        data.save()
        return redirect ("listProduct")


    return render (req,"editProduct.html", context)


def signUp(req):
    if req.method=='POST':
        username=req.POST.get("username")
        fullName=req.POST.get("fullName")
        email=req.POST.get("email")
        dateOfBirth=req.POST.get("dateOfBirth")
        if req.FILES.get("profileImage"):
            profileImage=req.FILES.get("profileImage")

 
        password=req.POST.get("password")
        user_types=req.POST.get("user_types")

        user=customerUser.objects.create_user(
            username=username,
            fullName=fullName,
            email=email,
            dateOfBirth=dateOfBirth,
            profileImage=profileImage,
            password=password,
            user_types=user_types,
        )
        return redirect('signIn')
    return render(req,'signUp.html')  

def signIn(req):
    if req.method=='POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        user= authenticate(req,username=username,password=password)
        if user:
            login(req,user)
            return redirect("home")
    return render(req,'signIn.html')
    

def logOut(req):
    logout(req)

    return redirect('signIn')    














