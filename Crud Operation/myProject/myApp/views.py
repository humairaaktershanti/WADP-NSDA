from django.shortcuts import render
from myApp.forms import *


def studentView(req):
    if req.method == 'POST':
        form = studentForm(req.POST).save()

        
    data = studentForm()
    context={
        'data': data
    }



    return render(req,'studentView.html',context)