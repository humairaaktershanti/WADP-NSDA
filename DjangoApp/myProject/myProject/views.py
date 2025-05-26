from django.shortcuts import render
from myApp.models import*

def homePage(req):
    return render(req,"index.html")

def studentTeacher(req):
    studentdata = student.objects.all()
    context={
        'data':studentdata,
    }
    return render(req,"studentTeacher.html",context)