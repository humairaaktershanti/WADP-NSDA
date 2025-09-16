from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime, timedelta
from .forms import UserRegistrationForm, UserProfileForm, ConsumedCalorieForm, CalorieGoalForm
from .models import UserProfile, ConsumedCalorie

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! Please complete your profile.')
            return redirect('profile_setup')
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
def profile_setup_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            profile.calculate_bmr()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile_setup.html', {'form': form})

@login_required
def dashboard_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_setup')
    
    # Get today's consumed calories
    today = date.today()
    consumed_calories = ConsumedCalorie.objects.filter(user=request.user, date=today)
    total_consumed = consumed_calories.aggregate(Sum('calories'))['calories__sum'] or 0
    
    # Calculate remaining calories
    if profile.daily_calorie_goal:
        remaining_calories = profile.daily_calorie_goal - total_consumed
    else:
        remaining_calories = None
    
    # Get recent consumed items
    recent_items = consumed_calories.order_by('-time')[:5]
    
    # Get data for the past 7 days
    past_week = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_calories = ConsumedCalorie.objects.filter(user=request.user, date=day).aggregate(Sum('calories'))['calories__sum'] or 0
        past_week.append({
            'date': day.strftime('%a'),
            'calories': day_calories
        })
    
    # Prepare form for adding consumed calories
    if request.method == 'POST':
        form = ConsumedCalorieForm(request.POST)
        if form.is_valid():
            consumed = form.save(commit=False)
            consumed.user = request.user
            consumed.save()
            messages.success(request, f'Added {consumed.item_name} with {consumed.calories} calories!')
            return redirect('dashboard')
    else:
        form = ConsumedCalorieForm()
    
    # Prepare form for setting calorie goal
    goal_form = CalorieGoalForm(instance=profile)
    
    context = {
        'profile': profile,
        'total_consumed': total_consumed,
        'remaining_calories': remaining_calories,
        'recent_items': recent_items,
        'past_week': past_week,
        'form': form,
        'goal_form': goal_form,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def set_calorie_goal_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_setup')
    
    if request.method == 'POST':
        form = CalorieGoalForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your daily calorie goal has been updated!')
            return redirect('dashboard')
    else:
        form = CalorieGoalForm(instance=profile)
    
    return render(request, 'set_calorie_goal.html', {'form': form})

@login_required
def calorie_history_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_setup')
    
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Default to last 7 days
    if not start_date:
        end_date_obj = date.today()
        start_date_obj = end_date_obj - timedelta(days=6)
    else:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date_obj = date.today()
    
    # Get consumed calories within the date range
    consumed_items = ConsumedCalorie.objects.filter(
        user=request.user,
        date__gte=start_date_obj,
        date__lte=end_date_obj
    ).order_by('-date', '-time')
    
    # Calculate daily totals
    daily_totals = {}
    for item in consumed_items:
        if item.date not in daily_totals:
            daily_totals[item.date] = 0
        daily_totals[item.date] += item.calories
    
    # Prepare data for chart
    chart_data = []
    current_date = start_date_obj
    while current_date <= end_date_obj:
        chart_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'calories': daily_totals.get(current_date, 0)
        })
        current_date += timedelta(days=1)
    
    context = {
        'profile': profile,
        'consumed_items': consumed_items,
        'chart_data': chart_data,
        'start_date': start_date_obj.strftime('%Y-%m-%d'),
        'end_date': end_date_obj.strftime('%Y-%m-%d'),
    }
    
    return render(request, 'calorie_history.html', context)

@login_required
def delete_consumed_item_view(request, item_id):
    item = get_object_or_404(ConsumedCalorie, id=item_id, user=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'Deleted {item.item_name} from your consumed items.')
        return redirect('dashboard')
    
    return render(request, 'delete_confirm.html', {'item': item})