from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout ,update_session_auth_hash
from .models import *
import random
import string

def loginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomUserModel.objects.get(email=email)
        if user.user_type == 'admin':
            if not user:
                messages.error(request, 'User with this email does not exist.')
                return redirect('dashboard_login')
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
             login(request, user_auth)
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid password. Please try again.')
            return redirect('dashboard_login')

    return render(request, 'auth/admin_login.html')


def dashboard_page(request):
    if request.user.is_authenticated:
        return render(request, 'admin_dashboard.html')
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('dashboard_login')
def logout_view(request):
    user_type = None
    if request.user.is_authenticated:
        user_type = request.user.user_type 


    logout(request)
    messages.success(request, 'You have been logged out.')

    if user_type == 'admin':
        return redirect('dashboard_login')

def guide_management(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        guide_requests = GuideRequestModel.objects.filter(status='pending')
        accepted_guides = GuideProfile.objects.all()  # all guides that have a profile
        context = {
            'guide_requests': guide_requests,
            'accepted_guides': accepted_guides
        }
        return render(request, 'guidelist.html', context)
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('dashboard_login')
    
