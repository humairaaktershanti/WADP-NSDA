from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from users_auth_app.models import*

# Create your views here.
# home_page
def home_page(request):
   
    return render(request, 'home_page.html')




# register
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        
        if username and phone and user_type:
            
            user=CustomUserModel.objects.create_user(
                username=username,
                password=phone,
                email=email,
                user_type=user_type,
        )
            if user:
                PendingAcountModel.objects.create(
                username=username,
                phone=phone,
                email=email,
                user_type=user_type,
                )
            
        
        return redirect('login_page')

    return render(request, 'register.html')

# Login view

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_type == 'admin':
                login(request, user)
            return redirect('home_page')
        else:
            login(request, user)
            return redirect('panding_list')
    return render(request, 'login.html')

# Logout view
def logout_page(request):
    logout(request)
    return redirect('login_page')


# changepass
def chnge_pass(request):
    curnt_user = request.user

    if request.method == 'POST':
        current_password = request.POST.get("current_password")
        confirm_password = request.POST.get("confirm_password")
        new_password = request.POST.get("new_password")

        if check_password(current_password, request.user.password):
          
            if new_password == confirm_password:
                curnt_user.set_password(new_password)  
                curnt_user.save()
                update_session_auth_hash(request, curnt_user)
                return redirect("login_page")

    return render(request, "change_pass.html")

# panding list

def panding_list(request):
    pandigUser=PendingAcountModel.objects.all()
    
    return render(request,'panding_list.html',{'pending':pandigUser})

def approveUser(request, id):
    if request.method == 'POST':
        panding=PendingAcountModel.objects.get(id=id)

        CustomUserModel.objects.create_user(
            username=panding.username,
            password=panding.phone,
            email=panding.email,
            user_type=panding.user_type,
        )
        panding.delete()
    return redirect('panding_list')

def Reject(request,id):
    if request.method =='POST':
        panding=PendingAcountModel.objects.get(id=id)
        panding.delete()
    return redirect('panding_list')



