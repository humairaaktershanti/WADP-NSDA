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
        name = request.POST.get('teacherName')
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

def TeacherList(request):

    Teacher = teacher.objects.all()
    context = {
        'teacher': Teacher
    }
    return render(request, 'TeacherList.html', context)



def addCourse(request):
    if request.method == 'POST':
        name = request.POST.get('courseName')
        department = request.POST.get('department')
        Code = request.POST.get('courseCode')
        credits = request.POST.get('credits')

        newCourse=course(
            name=name,
            department=department,
            Code=Code,
            credits=credits
        )

        newCourse.save()
        return redirect('courseList')
    return render(request, 'addCourse.html')

def courseList(request):

    Course = course.objects.all()
    context = {
        'course': Course
    }
    return render(request, 'courseList.html', context)