from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from users_auth_app.models import *



#----------Authenticate Functions
def registerpage(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        user_type=request.POST.get('user_type')
        pending_status=request.POST.get('pending_status')
        
        if user_type =='Admin':      
            CustomUserModel.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                password=phone,
                user_type ='Admin'
                )
        else:
            PendingAccountModel.objects.create(
                username=username,
                email=email,
                phone=phone,
                pending_user_type=user_type,
                pending_status='Pending',
            )
        return redirect('loginpage')
        
    return render(request, 'authenticate/registerpage.html')



#Function of loginpage
def loginpage(request):
    if request.method == 'POST':
       username=request.POST.get('username')
       password=request.POST.get('password')
       
       user = authenticate(request, username=username, password=password)
       
       if user:
           login(request, user)
           return redirect('dashboard')
    return render(request, 'authenticate/loginpage.html')


#Function of change_pass
def change_pass(request):
    current_user = request.user
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(oldpassword, request.user.password):
            if new_password == confirm_password:
                current_user.set_password(new_password) 
                current_user.save()
                update_session_auth_hash(request, current_user)
                return redirect('dashboard')
    return render(request, 'authenticate/change_pass.html')

#Function of LogOut
def logoutpage(request):
    logout(request)
    return redirect('loginpage')


#------------------pending urls

def dashboard(request):
    return render(request,'master/dashboard.html')


def list_pending(request):
    pending_data=PendingAccountModel.objects.all()
    context={
        'pending_data' :pending_data
    }
    return render(request,'pending/list_pending.html', context)
    



