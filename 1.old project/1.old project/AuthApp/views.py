from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User, Notification
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'employee':
                return redirect('employee_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'AuthApp/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'  # Only students can self-register
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'AuthApp/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'AuthApp/profile.html', {'form': form})

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    
    # Mark all as read when viewing
    for notification in notifications:
        if not notification.is_read:
            notification.is_read = True
            notification.save()
    
    return render(request, 'AuthApp/notifications.html', {'notifications': notifications})

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'employee':
        return redirect('employee_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')
    return redirect('login')

# Accesss super user to control

def is_superuser(user):
    return user.is_superuser

class AdminCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

@login_required
@user_passes_test(is_superuser)
def create_admin_view(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Admin account created successfully for {user.username}!')
            return redirect('create_admin')  # Stay on the same page to create more admins
    else:
        form = AdminCreationForm()
    
    return render(request, 'AuthApp/create_admin.html', {'form': form})


#create form and use here
class FirstAdminForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

def setup_view(request):
    # Check if any users already exist
    if User.objects.exists():
        messages.info(request, 'System is already set up. Please log in.')
        return redirect('login')
    
    if request.method == 'POST':
        form = FirstAdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create the superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin'
            )
            
            # Log the user in
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Admin account created successfully!')
                return redirect('admin_dashboard')
    else:
        form = FirstAdminForm()
    
    return render(request, 'AuthApp/setup.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel_view(request):
    """Redirect to Django admin panel"""
    return redirect('admin-panel/')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_admin_view(request):
    # Check if user has permission to create admins
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to create admin accounts.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Admin account created successfully for {user.username}!')
            return redirect('create_admin')  # Stay on the same page to create more admins
    else:
        form = AdminCreationForm()
    
    return render(request, 'AuthApp/create_admin.html', {'form': form})