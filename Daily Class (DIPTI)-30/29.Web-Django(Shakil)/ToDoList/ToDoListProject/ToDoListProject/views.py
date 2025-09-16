from django.shortcuts import render, redirect
from ToDoApp.models import *
from ToDoListProject.forms import *
from ToDoListProject.views import *
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

def signupPage(request):
    if request.method == 'POST':
        form = myUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Signup Successfully")
            return redirect('signinPage')
    else:
        form = myUserCreationForm(request.POST)
    
    context = {
        'form':form
    }
    
    return render(request,'signup.html',context)
            
def signinPage(request):
    
    if request.method == 'POST':
        signinForm = myAuthenticationForm(request,data = request.POST)
        if signinForm.is_valid():
            user = signinForm.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        signinForm = myAuthenticationForm()
    
    context = {
        'signinForm':signinForm
    }
    
    return render(request,'signin.html',context)

@login_required
def dashboard(request):
    
    
    return render(request,'dashboard.html')

def logoutPage(request):
    logout(request)
    
    return redirect('signinPage')