from django.shortcuts import render, redirect
from resumeApp.models import *

def formResume(req):
    if req.method == 'POST':
        fullName=req.POST.get('fullName')
        profilePicture=req.FILES.get('profilePicture')
        email=req.POST.get('email')
        phone=req.POST.get('phone')
        address=req.POST.get('address')
        summary=req.POST.get('summary')
        degree=req.POST.get('degree')
        instituteName=req.POST.get('instituteName')
        yearsOfGraduation=req.POST.get('yearsOfGraduation')
        companyName=req.POST.get('companyName')
        position=req.POST.get('position')
        yearsOfExperience=req.POST.get('yearsOfExperience')
        skills=req.POST.get('skills')
        hobbies=req.POST.get('hobbies')
        achievements=req.POST.get('achievements')


        resumeData=ResumeModel(
            fullName=fullName,
            profilePicture=profilePicture,
            email=email,
            phone=phone,
            address=address,
            summary=summary,
            degree=degree,
            instituteName=instituteName,
            yearsOfGraduation=yearsOfGraduation,
            companyName=companyName,
            position=position,
            yearsOfExperience=yearsOfExperience,
            skills=skills,
            hobbies=hobbies,
            achievements=achievements,
          
        )
        resumeData.save()

    return render(req,"formResume.html")



def listResume(req):
    resumeData=ResumeModel.objects.all()
    context={
        'resumeData':resumeData
    }

    return render(req,"listResume.html",context)


def deleteResume(req,id):
    resumeData=ResumeModel.objects.get(id=id).delete()
    return redirect('listResume')



def viewResume(req,id):
    resumeData=ResumeModel.objects.get(id=id)
    context={
        'resumeData':resumeData
    }

    return render(req,"viewResume.html",context)


def editResume(req,id):
    resumeData=ResumeModel.objects.get(id=id)
    context={
        'resumeData':resumeData
    }

    return render(req,"editResume.html",context)


def 