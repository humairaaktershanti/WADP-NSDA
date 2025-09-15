from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Sum

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    total_quantity = AddCash.objects.aggregate(total_sum=Sum('amount'))['total_sum']
    return render(request, 'index.html', {'data':total_quantity})

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def SignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user)
        AddCash.objects.create(user=user)
        Expense.objects.create(user=user)
        login(request, user)
        return redirect('logIn')
    
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect')
            return render(request, 'change_password.html')
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return render(request, 'change_password.html')
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('dashboard')
    
    return render(request, 'change_password.html')

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'update_profile.html', {'form': form})

@login_required
def logOut(request):
    logout(request)
    return redirect('index')

@login_required
def addCash(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = AddCashForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddCashForm(instance=profile)
    
    return render(request, 'addCash.html', {'form': form})

@login_required
def expense(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=profile)
    
    return render(request, 'expense.html', {'form': form})

@login_required
def Management_view(request):
    addCash = AddCash.objects.filter(user=request.user)
    expense = Expense.objects.filter(user=request.user)

    context = {
        'addCash':addCash,
        'expense':expense
    }
    return render(request, 'Management_view.html', context)