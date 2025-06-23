from django.shortcuts import render, redirect
from studentApp.models import *



def home(req):
    return render(req,"home.html")


def addStudent(req):
    if req.method=='POST':
        name=req.POST.get('name')
        roll_no=req.POST.get('roll_no')
        department=req.POST.get('department')
        student_image=req.FILES.get('student_image')

        data=studentModel(
            name=name,
            roll_no=roll_no,
            department=department,
            student_image=student_image

        )

        data.save()

        return redirect('studentList')

    return render(req,"addStudent.html")



def studentList(req):
    data=studentModel.objects.all()
    context={
        'data': data
    }
    return render(req,"studentList.html",context)


def viewStudent(req,id):
    data=studentModel.objects.get(id=id)
    context={
        'data':data
    }

    return render (req,"viewStudent.html",context)

def deleteStudent(req,id):
    data=studentModel.objects.get(id=id).delete()

    return redirect ('studentList')

def editStudent(req,id):
    data=studentModel.objects.get(id=id)
    context={
        'data':data
    }
    if req.method=='POST':
        name=req.POST.get('name')
        roll_no=req.POST.get('roll_no')
        department=req.POST.get('department')
        student_image=req.FILES.get('student_image')

        data=studentModel(
            id=id,
            name=name,
            roll_no=roll_no,
            department=department,
            student_image=student_image

        )

        data.save()

        return redirect('studentList')

    
    return render (req,"editStudent.html",context)








def addTask(req):
    if req.method=='POST':
        title=req.POST.get('title')
        description=req.POST.get('description')
        status=req.POST.get('status')
        due_date=req.POST.get('due_date')

        data=toDoModel(
            title=title,
            description=description,
            status=status,
            due_date=due_date,


        )
        data.save()

        return redirect('taskList')

    return render(req,"addTask.html")


def taskList(req):
    data=toDoModel.objects.all()
    context={
        'data': data
    }
    return render(req,"taskList.html",context)



def viewTask(req,id):
    data=toDoModel.objects.get(id=id)
    context={
        'data':data
    }

    return render (req,"viewTask.html",context)

def deleteTask(req,id):

    data=toDoModel.objects.get(id=id).delete()

    return redirect ('taskList')



def editTask(req,id):
    data=toDoModel.objects.get(id=id)
    context={
        'data':data
    }
    if req.method=='POST':
        title=req.POST.get('title')
        description=req.POST.get('description')
        status=req.POST.get('status')
        due_date=req.FILES.get('due_date')

        data=toDoModel(
            id=id,
            title=title,
            description=description,
            status=status,
            due_date=due_date

        )

        data.save()

        return redirect('taskList')

    
    return render (req,"editTask.html",context)