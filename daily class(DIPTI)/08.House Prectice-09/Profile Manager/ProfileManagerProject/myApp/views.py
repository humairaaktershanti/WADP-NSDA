from django.shortcuts import render,redirect

# Create your views here.
from .models import *

def formManager(req):
    if req.method=='POST':
        name=req.POST.get('name')
        date_of_birth=req.POST.get('date_of_birth')
        profile_photo=req.FILES.get('profile_photo')
        data=profileModel(
            name=name,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,


        )
        data.save()
        
        return redirect ("listManager")



    return render (req,"formManager.html")

def listManager(req):
    data=profileModel.objects.all()
    context={
        'data':data
    }
    return render(req,"listManager.html",context)


def updateManager(req,id):
    data=profileModel.objects.get(id=id)
    context={

        'data':data
    }


    if req.method=='POST':
        name=req.POST.get('name')
        date_of_birth=req.POST.get('date_of_birth')
        profile_photo=req.FILES.get('profile_photo')
        data=profileModel(
            id=id,
            name=name,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,


        )
        data.save()
        return redirect ("formManager")

    return render(req,'updateManager.html',context)


    