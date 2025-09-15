from django.shortcuts import render, redirect

# Create your views here.
from courseApp.models import *

def home(req):
    return render(req,"home.html")

def addCourse(req):
    if req.method == 'POST':
        name=req.POST.get('name')
        duration=req.POST.get('email')
        description=req.POST.get('description')

        data=courseModel(
            name=name,
            duration=duration,
            description=description,
        )
        data.save()
        return redirect('listCourse')

    return render(req,"addCourse.html")

def listCourse(req):
    data=courseModel.objects.all()
    
    context={

        'data': data
    }

    return render(req,"listCourse.html",context)

def viewCourse(req,id):
    data=courseModel.objects.get(id=id)
    context={
        'data': data
    }
    return render(req,"viewCourse.html",context)

def deleteCourse(req,id):
  data=courseModel.objects.get(id=id).delete()
  return redirect ('listCourse')

def editCourse(req,id):
    data=courseModel.objects.get(id=id)
    context={
        'data': data
    }
    if req.method == 'POST':
        data.id=id
        data.name=req.POST.get('name')
        data.duration=req.POST.get('duration')
        data.description=req.POST.get('description')

        data.save()
        return redirect('listCourse')
    return render(req,"editCourse.html",context)