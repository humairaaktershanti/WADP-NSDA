from django.shortcuts import render,redirect
from myApp.models import *

def candidatePage(request):
    candidate=candidateModel.objects.all()
    candict={
        'candidate':candidate
    }
    return render(request,'candidate.html',candict)

def addcandidate(request):
    if request.method=='POST':
        fname=request.POST.get('fullnane')
        eamil=request.POST.get('email')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')
        title=request.POST.get('title')
        lprofile=request.POST.get('lprofile')
        university=request.POST.get('university')
        degree=request.POST.get('degree')
        languages=request.POST.get('languages')
        experience=request.POST.get('experience')
       
        addcand=candidateModel(
            full_name=fname,
            email=eamil,
            phone_number=mobile,
            address=address,
            job_title=title,
            linkedin_profile=lprofile,
            university=university,
            degree=degree,
            languages=languages,
            years_of_experience=experience,
        )
        addcand.save()
        return redirect('candidatePage')
    return render(request,'addcandidate.html')

def deleteCandidate(request,myid):
    delcandidate=candidateModel.objects.get(id=myid)
    delcandidate.delete()
    return redirect('candidatePage')
    

def editCandidate(request,myid):
    candidate=candidateModel.objects.get(id=myid)
    
    candict={
        'candidate':candidate
    }
    return render(request,'editcandidate.html',candict)

def updatecandidate(request):
    if request.method=='POST':
        cid=request.POST.get('cid')
        fname=request.POST.get('fullnane')
        eamil=request.POST.get('email')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')
        title=request.POST.get('title')
        lprofile=request.POST.get('lprofile')
        university=request.POST.get('university')
        degree=request.POST.get('degree')
        languages=request.POST.get('languages')
        experience=request.POST.get('experience')
       
        addcand=candidateModel(
            id=cid,
            full_name=fname,
            email=eamil,
            phone_number=mobile,
            address=address,
            job_title=title,
            linkedin_profile=lprofile,
            university=university,
            degree=degree,
            languages=languages,
            years_of_experience=experience,
        )
        addcand.save()
        return redirect('candidatePage')
    
def viewCandidate(request,myid):
    candidate=candidateModel.objects.get(id=myid)
    candict={
        'candidate':candidate
    }
    return render(request,'viewcandidate.html',candict)