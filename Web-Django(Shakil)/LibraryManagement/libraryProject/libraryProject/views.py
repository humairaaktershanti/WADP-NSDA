from django.shortcuts import redirect, render
from libraryApp.models import *
from django.contrib.auth import authenticate,login,logout

def signupPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        address=request.POST.get('address')
        user_type=request.POST.get('user_type')
        
        if password == confirm_password:
            user=Llibrary_User.objects.create_user(username=username,password=password)
            user.FullName = fullname
            user.email = email
            user.Address= address
            user.UserType = user_type
            user.save()
            return redirect('signinPage')
    return render(request,'signup.html')

def signinPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            return redirect('signinPage')
    
    return render(request,'signin.html')

def dashboard(request):
    
    return render(request,'dashboard.html')


