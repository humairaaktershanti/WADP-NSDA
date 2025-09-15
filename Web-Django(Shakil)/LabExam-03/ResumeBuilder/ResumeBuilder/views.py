from django.shortcuts import render, redirect
from ResumeApp.models import *

def resume(request):
    resumedata=resumeInfoModel.objects.all()
    resumedict={
        'resumedata':resumedata,
    }
    return render(request,'resume.html',resumedict)

def addresume(request):
    if request.method=='POST':
        fullname=request.POST.get('fullname')
        address=request.POST.get('address')
        phonenumber=request.POST.get('phonenumber')
        email=request.POST.get('email')
        careerobj=request.POST.get('careerobj')
        degree=request.POST.get('degree')
        institute=request.POST.get('institute')
        graduation=request.POST.get('graduation')
        company=request.POST.get('company')
        position=request.POST.get('position')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        skills=request.POST.get('skills')
        project=request.POST.get('project')
        certifications=request.POST.get('certifications')
        references=request.POST.get('references')
        profileimage=request.FILES.get('profileimage')
        
        resumeinfo=resumeInfoModel(
            ProfileImage=profileimage,
            FullName=fullname,
            Address=address,
            PhoneNumber=phonenumber,
            EmailAddress=email,
            CareerObjective=careerobj,
            Skills=skills,
            Certifications=certifications,
            Projects=project,
            References=references
        )
        
        
        educationinfo=educationModel(
            FullName=fullname,
            Degree=degree,
            institute=institute,
            graduation=graduation,
        )
        workinfo=workModel(
            FullName=fullname,
            Company=company,
            Position=position,
            StartDate=startdate,
            EndDate=enddate
        )
        resumeinfo.save()
        educationinfo.save()
        workinfo.save()
        return redirect('resume')
    return render(request,'addresume.html')

def viewresume(request,myid):
    infodata=resumeInfoModel.objects.get(id=myid)
    
    workdata=workModel.objects.get(id=myid)
    educationdata=educationModel.objects.get(id=myid)
    print(infodata.FullName)
    datadict={
        'infodata':infodata,
        'workdata':workdata,
        'educationdata': educationdata,
    }
    return render(request,'viewresume.html',datadict)


def editresume(request,myid):
    infodata=resumeInfoModel.objects.get(id=myid)
    workdata=workModel.objects.get(id=myid)
    educationdata=educationModel.objects.get(id=myid)
    print(infodata.FullName)
    datadict={
        'infodata':infodata,
        'workdata':workdata,
        'educationdata': educationdata,
    }
    return render(request,'editresume.html',datadict)

def updateresume(request):
    if request.method=='POST':
        fullname=request.POST.get('fullname')
        resumeid=request.POST.get('resumeid')
        address=request.POST.get('address')
        phonenumber=request.POST.get('phonenumber')
        email=request.POST.get('email')
        careerobj=request.POST.get('careerobj')
        degree=request.POST.get('degree')
        institute=request.POST.get('institute')
        graduation=request.POST.get('graduation')
        company=request.POST.get('company')
        position=request.POST.get('position')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        skills=request.POST.get('skills')
        project=request.POST.get('project')
        certifications=request.POST.get('certifications')
        references=request.POST.get('references')
        previmage=request.POST.get('previmage')
        profileimage=request.FILES.get('profileimage')
        
        if profileimage==None:
            resumeinfo=resumeInfoModel(
                id=resumeid,
                ProfileImage=previmage,
                FullName=fullname,
                Address=address,
                PhoneNumber=phonenumber,
                EmailAddress=email,
                CareerObjective=careerobj,
                Skills=skills,
                Certifications=certifications,
                Projects=project,
                References=references
                )
        else:
            resumeinfo=resumeInfoModel(
                id=resumeid,
                ProfileImage=profileimage,
                FullName=fullname,
                Address=address,
                PhoneNumber=phonenumber,
                EmailAddress=email,
                CareerObjective=careerobj,
                Skills=skills,
                Certifications=certifications,
                Projects=project,
                References=references
                )
        
        educationinfo=educationModel(
            FullName=fullname,
            Degree=degree,
            institute=institute,
            graduation=graduation,
        )
        workinfo=workModel(
            FullName=fullname,
            Company=company,
            Position=position,
            StartDate=startdate,
            EndDate=enddate
        )
        

        resumeinfo.save()
        educationinfo.save()
        workinfo.save()
        return redirect('resume')

def deleteresume(request,myid):
    infodata=resumeInfoModel.objects.get(id=myid)
    workdata=workModel.objects.get(id=myid)
    edudata=educationModel.objects.get(id=myid)
    
    infodata.delete()
    workdata.delete()
    edudata.delete()
    return redirect('resume')