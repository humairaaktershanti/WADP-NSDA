from django.shortcuts import render,redirect
from user_auth.models import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def register(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        phone= req.POST.get('phone')
        password = req.POST.get('password')
        user_type = req.POST.get('usertype')

        if user_type == 'Admin':
            customUserModel.objects.create_user(
                username=username,
                email=email,
                password=phone,
                phone=phone,
                user_type='Admin'
            )

        else:
            PendingAccountModel.objects.create(
                username=username,
                email=email,
                phone=phone,
                user_type=user_type,
                profile_status='Pending'
            )
            return redirect(req, 'login_page.html')

    return render(req,'register_page.html')


def loginpage(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user:
            login(req, user)

            
        return redirect(req, 'dashboard.html')
    return render(req,'login_page.html')


def dashboard(req):
    return render(req, 'dashboard.html')