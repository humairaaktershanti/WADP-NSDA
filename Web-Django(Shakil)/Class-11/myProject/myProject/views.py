from django.shortcuts import render, redirect
from myApp.models import *

def studentpage(request):
    student = studentModel.objects.all()
    studic={
        'std':student
    }
    return render(request, 'student.html',studic)

def addstudent(request):
    if request.method=='POST':
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        dept=request.POST.get('department')
        
        addstd=studentModel(
            FirstName=fname,
            LastName=lname,
            Department=dept,
        )
        addstd.save()
        return redirect('studentpage')
        
    return render(request,'addstudent.html')

def deletestudent(request,myid):
    delstudent = studentModel.objects.get(id=myid)
    delstudent.delete()
    return redirect('studentpage')

def editstudent(request, myid):
    student=studentModel.objects.filter(id=myid)
    stddic={
        'student':student
    }

    return render(request,'editstudent.html',stddic)

def updatestudent(request):
    if request.method=='POST':
        
        myid=request.POST.get('id')
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        dept=request.POST.get('department')
        
        addstd=studentModel(
            id=myid,
            FirstName=fname,
            LastName=lname,
            Department=dept,
        )
        addstd.save()
        return redirect('studentpage')
    
def viewstudent(request,myid):
    student=studentModel.objects.filter(id=myid)
    stdic={
        'student':student
    }
    return render(request,'viewstudent.html',stdic)