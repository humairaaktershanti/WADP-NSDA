from django.shortcuts import render, redirect
from studentApp.models import *
from studentApp.models import *

def addStudent(request):
    if request.method == 'POST':
        name = "request.POST.get('studentName')"
        department = request.POST.get('department')
        city = request.POST.get('cityName')
        age = request.POST.get('studentAge')

        newstudent=student(
            name=name,
            department=department,
            city=city,
            age=age
        )

        newstudent.save()
        return redirect('studentList')
    return render(request, 'addStudent.html')

def home(request):
    return render(request, 'home.html')

def studentList(request):

    students = student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'studentList.html', context)

def addTeacher(request):
    if request.method == 'POST':
        name = "request.POST.get('teacherName')"
        department = request.POST.get('department')
        city = request.POST.get('cityName')
        age = request.POST.get('teacherAge')

        newteacher=teacher(
            name=name,
            department=department,
            city=city,
            age=age
        )

        newteacher.save()
        return redirect('TeacherList')
    return render(request, 'addTeacher.html')

def TeacherList(req):
    return render(req, 'TeacherList.html')