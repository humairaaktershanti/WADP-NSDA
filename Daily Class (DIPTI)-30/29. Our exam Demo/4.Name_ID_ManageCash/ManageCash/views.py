from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import UserRegistrationForm, AddCashForm, ExpenseForm
from .models import AddCash, Expense

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

@login_required
def dashboard_view(request):
    # Calculate totals
    total_cash = AddCash.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_cash - total_expenses
    
    # Get recent transactions
    recent_cash = AddCash.objects.filter(user=request.user).order_by('-datetime')[:5]
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-datetime')[:5]
    
    context = {
        'total_cash': total_cash,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_cash': recent_cash,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def add_cash_view(request):
    if request.method == 'POST':
        form = AddCashForm(request.POST)
        if form.is_valid():
            cash_entry = form.save(commit=False)
            cash_entry.user = request.user
            cash_entry.save()
            messages.success(request, 'Cash entry added successfully!')
            return redirect('dashboard')
    else:
        form = AddCashForm()
    return render(request, 'add_cash.html', {'form': form})

@login_required
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})