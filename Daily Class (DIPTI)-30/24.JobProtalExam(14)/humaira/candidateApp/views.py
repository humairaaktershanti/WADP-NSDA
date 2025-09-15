from django.shortcuts import render
from .models import *

def newJobApplication(req):
    data = jobApplicatonModel.objects.all()
    context={
        'data' : data
    }
    return render(req,"newJobApplication.html",context)