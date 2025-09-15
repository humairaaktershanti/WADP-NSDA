from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Activity, RoleChoices  # Assumed models
from django.db.models import Q

# -----------------------------
# First-time setup for Admin
# -----------------------------
def setup_view(request):
    if User.objects.exists():
        return redirect('login')  # If users exist, skip setup

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('setup')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists!")
            return redirect('setup')

        user = User.objects.create_user(username=username, email=email, password=password1, is_superuser=True, is_staff=True)
        Profile.objects.create(user=user, role='admin')  # assuming Profile model with role field
        messages.success(request, "Admin account created successfully!")
        login(request, user)
        return redirect('admin_dashboard')

    return render(request, 'setup.html')


# -----------------------------
# Login View
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.profile.role  # Assuming user has profile with role field
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'hr':
                return redirect('hr_dashboard')
            elif role == 'faculty':
                return redirect('faculty_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            elif role == 'candidate':
                return redirect('candidate_dashboard')
            else:
                messages.error(request, "Role not assigned!")
                logout(request)
                return redirect('login')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'login.html')


# -----------------------------
# Signup View (Student Only)
# -----------------------------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.create(user=user, role='student')
        messages.success(request, "Account created successfully!")
        login(request, user)
        return redirect('student_dashboard')

    return render(request, 'register.html')


# -----------------------------
# Logout View
# -----------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# -----------------------------
# Dashboard Views (Role-Based)
# -----------------------------
@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        messages.error(request, "Access denied!")
        return redirect('login')
    return render(request, 'dashboards/admin_dashboard.html')


@login_required
def hr_dashboard(request):
    if request.user.profile.role != 'hr':
        messages.error(request, "Access denied!")
        return redirect('login')
    return render(request, 'dashboards/hr_dashboard.html')


@login_required
def faculty_dashboard(request):
    if request.user.profile.role != 'faculty':
        messages.error(request, "Access denied!")
        return redirect('login')
    return render(request, 'dashboards/faculty_dashboard.html')


@login_required
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "Access denied!")
        return redirect('login')
    return render(request, 'dashboards/teacher_dashboard.html')


@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        messages.error(request, "Access denied!")
        return redirect('login')
    return render(request, 'dashboards/student_dashboard.html')


@login_required
def candidate_dashboard(request):
    if request.user.profile.role != 'candidate':
        messages.error(request, "Access denied!")
        return redirect('login')
    return render(request, 'dashboards/candidate_dashboard.html')


# -----------------------------
# Profile Management
# -----------------------------
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')

        if User.objects.filter(Q(username=username) & ~Q(pk=user.pk)).exists():
            messages.error(request, "Username already exists!")
            return redirect('edit_profile')

        if User.objects.filter(Q(email=email) & ~Q(pk=user.pk)).exists():
            messages.error(request, "Email already exists!")
            return redirect('edit_profile')

        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('edit_profile')

    return render(request, 'profile/edit_profile.html')
