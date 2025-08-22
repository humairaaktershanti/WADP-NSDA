from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import *


# -------------------------
# First-time Setup (Admin)
# -------------------------
def setupPage(request):
    if User.objects.filter(role='admin').exists():
        return redirect('loginPage')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('setupPage')

        user = User.objects.create_superuser(username=username, email=email, password=password1, role='admin')
        messages.success(request, "Admin account created. Please login.")
        return redirect('loginPage')

    return render(request, 'setup.html')





# -------------------------
# Student Registration
# -------------------------
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1, role='student')
        messages.success(request, "Account created successfully. Please login.")
        return redirect('loginPage')

    return render(request, 'registerPage.html')


# -------------------------
# Login View
# -------------------------
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('index')

    if not User.objects.filter(role='admin').exists():
        return redirect('setupPage')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    return render(request,'loginPage.html')


# -------------------------
# Logout View
# -------------------------
@login_required
def logoutPage(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('loginPage')

    
def index(request):
    return render(request, 'index.html')


def profileInfo(request):
    User.objects.all()
    return render(request, 'profileInfo.html')

@login_required
def editProfile(request):
    user = request.user  # Get currently logged-in user

    if request.method == 'POST':
        image = request.FILES.get('image')
        bio = request.POST.get('bio')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        country = request.POST.get('country')
        phone = request.POST.get('phone')

        # Update fields
        if image:
            user.image = image
        user.bio = bio
        user.date_of_birth = date_of_birth or None
        user.gender = gender
        user.location = location
        user.country = country
        user.phone = phone

        user.save()  # Save updates
        messages.success(request, "Profile updated successfully")
        return redirect('profileInfo')

    return render(request, 'editProfile.html', {"user": user})



def changePasswordPage(request):
    current_user = request.user
    if request.method == 'POST':
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')

        if check_password(oldPassword, current_user.password):
            if newPassword == confirmPassword:
                current_user.set_password(newPassword)
                current_user.save()
                update_session_auth_hash(request,current_user)
                return redirect('profileInfo')
    return render(request, 'changePasswordPage.html')





# -------------------------
# Dashboard Redirect Based on Role
# -------------------------
# def index_view(request):
#     role = request.user.role
#     if role == 'admin':
#         return redirect('admin_dashboard')
#     elif role == 'faculty':
#         return redirect('faculty_dashboard')
#     elif role == 'teacher':
#         return redirect('teacher_dashboard')
#     elif role == 'student':
#         return redirect('student_dashboard')
#     elif role == 'candidate':
#         return redirect('candidate_dashboard')
#     elif role == 'employee':
#         return redirect('employee_dashboard')
#     else:
#         return render(request, 'index.html', {'user': request.user})
