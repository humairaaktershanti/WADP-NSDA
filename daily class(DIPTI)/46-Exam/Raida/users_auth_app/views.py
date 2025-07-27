from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from users_auth_app.models import *

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib import messages
from users_auth_app.models import CustomUserModel

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user_type = request.POST.get('user_type')

        user_type = user_type if user_type in ['Admin', 'Employer', 'Candidate'] else 'Candidate'


        
        user = CustomUserModel.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            user_type=user_type,
            password=phone  
        )

        if user_type == 'Admin':
            messages.success(request, 'Admin registered successfully! Please log in.')
            return redirect('loginPage')
        else:
            messages.error(request, 'User registered and is pending approval.')
            return redirect('pendingAccount')

    return render(request, 'authenticate/registerPage.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('phone')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboardPage')
        else:
            messages.error(request, 'Invalid username or phone (password).')

    return render(request, 'authenticate/loginPage.html')




def changePasswordPage(request):
    current_user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password and new_password and confirm_password:
            if check_password(current_password, current_user.password):
                if new_password == confirm_password:
                    current_user.set_password(new_password)
                    current_user.save()
                    update_session_auth_hash(request, current_user) 
                    messages.success(request, 'Password changed successfully.')
                    return redirect('dashboardPage')
                else:
                    messages.error(request, "New password and confirmation don't match.")
            else:
                messages.error(request, "Current password is incorrect.")
        

    return render(request, 'authenticate/changePasswordPage.html')



def dashboardPage(request): 
    return render(request, 'master/dashboardPage.html')


def pendingAccount(request):
    pending_accounts = PendingAccountModel.objects.filter(pending_status='Pending')
    return render(request, 'pending/pendingAccount.html', {'pending_accounts': pending_accounts})


def approve_account(request, a_id):
    pending = PendingAccountModel.objects.get(id=a_id)

    user = CustomUserModel.objects.create_user(
            username=pending.username,
            email=pending.email,
            phone=pending.phone,
            user_type=pending.user_type,
            password=pending.phone  
        )
    pending.delete()
    return redirect('pendingAccount')



def logoutPage(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('loginPage')