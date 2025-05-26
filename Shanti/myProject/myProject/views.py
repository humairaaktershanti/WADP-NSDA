from django.shortcuts import render
from myApp.models import*

def homePage(req):
    studentData = student.objects.all()
    context = {
        'data': studentData
    }
    return render(req, "index.html", context)


def loginPage(req):
    return render(req,"loginPage.html")

def signupPage(req):
    return render(req,"signupPage.html")