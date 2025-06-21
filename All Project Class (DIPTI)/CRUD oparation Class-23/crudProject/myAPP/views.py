from django.shortcuts import render, redirect
from .models import *


# Create your views here.


def create(req):

    if req.method=='POST':
        name=req.POST.get('name')
        image=req.FILES.get('image')

        data=CrudModel(
            name=name,
            image=image
        )
        data.save()
        return redirect ('read')

    return render(req,"create.html")

def read(req):
    data=CrudModel.objects.all()
    context={
        'data': data
    }
    return render(req,"read.html",context)



def edit(req,id):
    data=CrudModel.objects.get(id=id)
    context={
        'data': data
    }

    if req.method=='POST':
        name=req.POST.get('name')
        image=req.FILES.get('image')

        data=CrudModel(
            id=id,
            name=name,
            image=image,
        )
        data.save()
        return redirect ('read')

    return render(req,'edit.html',context)


def delete(req,id):
    CrudModel.objects.get(id=id).delete()
    return redirect ('read')