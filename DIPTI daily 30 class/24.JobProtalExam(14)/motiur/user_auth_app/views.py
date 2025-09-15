from django.shortcuts import render

from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from user_auth_app.models import *
from employer_app.models import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash


@login_required
def dashboard(req):
    return render(req, 'dashboard.html',)

def register(req):
    if req.method == 'POST':
        username= req.POST.get('username')
        email= req.POST.get('email')
        phone= req.POST.get('phone')
        user_types= req.POST.get('user_types')
        
        if user_types=='Admin':
            CustomUserModel.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                user_types='Admin',
                password=phone,
            )

        else:
            PendingAccountModel.objects.create(
                username=username,
                email=email,
                phone=phone,
                user_types=user_types,
                pending_status='Pending',
            )

        return redirect('signin')

    return render(req, 'register.html')

def signin(req):
    if req.method == 'POST':
        username= req.POST.get('username')
        password= req.POST.get('password')
        user= authenticate(username=username,password=password)
        if user:
            login(req, user)
            return redirect ('dashboard')
        else:
            return HttpResponse('wrong data')
        
    return render(req, 'signin.html')

def change_pass(req):
    current_user=req.user
    if req.method=='POST':
        old_password=req.POST.get('old_password')
        new_password=req.POST.get('new_password')
        confirm_password=req.POST.get('confirm_password')
        if check_password(old_password,req.user.password):
            if new_password==confirm_password:
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(req,current_user)
                return redirect('dashboard')
            else:
                return HttpResponse('new password do not match')
        else:
            return HttpResponse('old password do not match')
    return render(req,'change_pass.html')

def signout(req):
    logout(req)
    return redirect ('signin')

def pending_account(req):
    data= PendingAccountModel.objects.filter(pending_status='Pending')
    context={
        'data': data
    }
    return render(req,'pending_account.html', context)


def approve_account(re, id):
    pending = PendingAccountModel.objects.get(id=id)

    user = CustomUserModel.objects.create_user(
        username=pending.username,
        email=pending.email,
        phone=pending.phone,
        user_types=pending.user_types,
        password=pending.phone
    )
    pending.delete()
    return redirect('pending_account')





def update_employer_profile(req):
    profile = EmployerProfileModel.objects.get(employer=req.user)

    # if req.method == 'POST':
    #     profile.company_name = req.POST('company_name')
    #     profile.about_company = req.POST('about_company')
    #     profile.location = req.POST('location')

    #     if 'company_logo' in req.FILES:
    #         profile.company_logo = req.FILES('company_logo')

    #     profile.save()
    #     return redirect('dashboard')

    return render(req, 'update_employer_profile.html', {'profile': profile})