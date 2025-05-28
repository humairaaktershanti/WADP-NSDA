from django.shortcuts import render
from ProductApp.models import*

def home(req):
    return render(req,"home.html")

def products(req):
    return render(req,"products.html")

def addProduct(req):
    return render(req,"addProduct.html")

