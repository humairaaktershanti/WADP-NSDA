from django.shortcuts import render, redirect
from myApp.models import *

def studentPage(request):
    student=studetnModel.objects.all()
    studata={
        'std':student
    }
    return render(request, 'student.html',studata)

def addStudent(request):
    if request.method=='POST':
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        dep=request.POST.get('department')
        city=request.POST.get('city')
        
        student= studetnModel(
            FirstName=fname,
            LastName=lname,
            Department=dep,
            City=city,
        )
        student.save()
        return redirect('studentPage')
    return render(request, 'addstudent.html')

def teacherPage(request):
    teacher=teacherModel.objects.all()
    techdata={
        'tech':teacher
    }
    return render(request, 'teacher.html',techdata)

def addTeacher(request):
    if request.method=='POST':
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        dep=request.POST.get('department')
        city=request.POST.get('city')
        
        teacher= teacherModel(
            FirstName=fname,
            LastName=lname,
            Department=dep,
            City=city,
        )
        teacher.save()
        return redirect('teacherPage')
    return render(request, 'addteacher.html')