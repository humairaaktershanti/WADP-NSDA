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

def editstudent(request):
    pass