from django.shortcuts import render,redirect
from courseApp.models import *
from courseApp.forms import *


# Create your views here.
def addCourse(req):
    if req.method=='POST':
        form=addCourseForms(req.POST)
        courseTitle=form.cleaned_data['courseTitle']
        courseDescription=form.cleaned_data['courseDescription']
        courseDuration=form.cleaned_data['courseDuration']
        courseStartDate=form.cleaned_data['courseStartDate']
        courseFee=form.cleaned_data['courseFee']

        course=courseModel(
            assignTeacher=req.user.teacherName,
            courseTitle=courseTitle,
            courseDescription=courseDescription,
            courseDuration=courseDuration,
            courseStartDate=courseStartDate,
            courseFee=courseFee,

        )
        course.save()
        return redirect('listCourse')


    data=addCourseForms()
    context={
        'data':data
    }
    
    return render(req, 'addCourse.html',context)

def addAdmitted(req):
    data=addAdmittedForms()
    context={
        'data':data
    }

    return render(req,'addAdmitted.html',context)
 
