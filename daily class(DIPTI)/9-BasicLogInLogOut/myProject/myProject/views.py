from django.shortcuts import render
from myApp.models import*

# def homePage(req):
#     return render(req, "index.html")


def loginPage(req):
    return render(req,"loginPage.html")

def signupPage(req):
    return render(req,"signupPage.html")

def contactPage(req):
    return render(req,"contactPage.html")

def newsPage(req):
    return render(req,"newsPage.html")

def aboutPage(req):
    return render(req,"aboutPage.html")

def homePage(req):
    return render(req,"homePage.html")
