from django.shortcuts import render, redirect

# Create your views here.
from inventoryApp.models import *

def home(req):
    return render(req,"home.html")

def addSupplier(req):
    if req.method == 'POST':
        name=req.POST.get('name')
        email=req.POST.get('email')
        phone=req.POST.get('phone')

        data=supplierModel(
            name=name,
            email=email,
            phone=phone,
        )
        data.save()
        return redirect('listSupplier')

    return render(req,"addSupplier.html")

def listSupplier(req):
    data=supplierModel.objects.all()
    
    context={

        'data': data
    }

    return render(req,"listSupplier.html",context)

def viewSupplier(req,id):
    data=supplierModel.objects.get(id=id)
    context={
        'data': data
    }
    return render(req,"viewSupplier.html",context)

def deleteSupplier(req,id):
  data=supplierModel.objects.get(id=id).delete()
  return redirect ('listSupplier')

def editSupplier(req,id):
    data=supplierModel.objects.get(id=id)
    context={
        'data': data
    }
    if req.method == 'POST':
        data.id=id
        data.name=req.POST.get('name')
        data.email=req.POST.get('email')
        data.phone=req.POST.get('phone')

        data.save()
        return redirect('listSupplier')
    return render(req,"editSupplier.html",context)