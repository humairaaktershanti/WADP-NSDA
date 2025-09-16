from django.shortcuts import render, redirect
from customUserAuth.models import CustomUserAuthModel
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from adminApp.models import ActivityLogModel


# Create your views here.
def homePage(request):
    return render(request, 'landing_page/index2.html')

def signUp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if CustomUserAuthModel.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        CustomUserAuthModel.objects.create_user(
            username=email,
            password=password,
            user_types='Admin',
        )
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('logIn')

    return render(request, 'register.html')


def logIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_types == 'Admin':
                return redirect('dashboard')
            elif user.user_types == 'Employee':
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'login.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        if not user.check_password(old_password):
            messages.warning(request, "Old password is incorrect.")
        elif new_password1 != new_password2:
            messages.warning(request, "New password and confirm password do not match.")
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user) 
            messages.success(request, "Your password has been updated successfully.")
            return redirect('change_password') 
    return render(request, 'change-password.html')

@login_required
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

@login_required
def logOut(request):
    if request.user.is_authenticated:
        ActivityLogModel.objects.create(
            user=request.user,
            action='logout',
            model_name='User',
            object_repr=str(request.user),
            ip_address=get_client_ip(request)
        )
        logout(request)
    return redirect('logIn')

@login_required
def lock_screen(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user

        # Verify password
        if user.check_password(password):
            login(request, user)
            return redirect("dashboard") 
        else:
            messages.error(request, "Incorrect password. Please try again.")

    return render(request, "lock-screen.html")