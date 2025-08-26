from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from AuthApp.models import User, Notification
from EmployeeApp.models import Course, Attendance, Transaction
from StudentApp.models import Enrollment
from .models import Event, Notice
from .forms import EventForm, NoticeForm

from AuthApp.forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth import get_user_model
from django.contrib import admin

from django.contrib.auth import views as auth_views


User = get_user_model()

def is_admin(user):
    return user.role == 'admin'

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_site_view(request):
    """
    Custom admin site view that checks if the user is a superuser
    """
    if not request.user.is_superuser:
        return render(request, 'AdminApp/admin_access_denied.html')
    
    # If the user is a superuser, redirect to the actual admin site
    return admin.site.index()

# Custom admin login view
def admin_login_view(request, **kwargs):
    """
    Custom admin login view that only allows superusers
    """
    response = auth_views.LoginView.as_view(**kwargs)(request)
    
    # After successful login, check if the user is a superuser
    if request.user.is_authenticated and not request.user.is_superuser:
        from django.contrib.auth import logout
        logout(request)
        return render(request, 'AdminApp/admin_access_denied.html')
    
    return response

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    # Get unread notifications count
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    # Summary data
    total_students = User.objects.filter(role='student').count()
    active_students = User.objects.filter(role='student', is_active=True).count()
    
    total_teachers = User.objects.filter(role='employee', sub_role='teacher').count()
    active_teachers = User.objects.filter(role='employee', sub_role='teacher', is_active=True).count()
    
    total_courses = 0  # Will be calculated when Course model is available
    active_courses = 0  # Will be calculated when Course model is available
    
    total_staff = User.objects.filter(role='employee').exclude(sub_role='teacher').count()
    active_staff = User.objects.filter(role='employee').exclude(sub_role='teacher').filter(is_active=True).count()
    
    # Recent activities
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Financial summary
    total_earnings = 0  # Will be calculated when Transaction model is available
    total_expenses = 0  # Will be calculated when Transaction model is available
    
    # Recent notices
    recent_notices = []  # Will be populated when Notice model is available
    
    context = {
        'total_students': total_students,
        'active_students': active_students,
        'inactive_students': total_students - active_students,
        'total_teachers': total_teachers,
        'active_teachers': active_teachers,
        'inactive_teachers': total_teachers - active_teachers,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'inactive_courses': total_courses - active_courses,
        'total_staff': total_staff,
        'active_staff': active_staff,
        'inactive_staff': total_staff - active_staff,
        'recent_users': recent_users,
        'total_earnings': total_earnings,
        'total_expenses': total_expenses,
        'recent_notices': recent_notices,
        'unread_notifications_count': unread_count,
    }
    
    return render(request, 'AdminApp/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def users(request):
    users = User.objects.all().order_by('role', 'sub_role', 'username')
    context = {'users': users}
    return render(request, 'AdminApp/users.html', context)

@login_required
@user_passes_test(is_admin)
def courses(request):
    courses = Course.objects.all().order_by('status', 'title')
    context = {'courses': courses}
    return render(request, 'AdminApp/courses.html', context)

@login_required
@user_passes_test(is_admin)
def attendance(request):
    # Get last 7 days attendance data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)
    
    attendance_data = Attendance.objects.filter(date__range=[start_date, end_date]).order_by('date')
    
    # Group by date and attendee type
    attendance_summary = {}
    for date in (start_date + timedelta(days=i) for i in range(8)):
        date_str = date.strftime('%Y-%m-%d')
        attendance_summary[date_str] = {
            'date': date,
            'students_present': Attendance.objects.filter(date=date, attendee_type='student', status='present').count(),
            'students_absent': Attendance.objects.filter(date=date, attendee_type='student', status='absent').count(),
            'teachers_present': Attendance.objects.filter(date=date, attendee_type='teacher', status='present').count(),
            'teachers_absent': Attendance.objects.filter(date=date, attendee_type='teacher', status='absent').count(),
            'staff_present': Attendance.objects.filter(date=date, attendee_type='staff', status='present').count(),
            'staff_absent': Attendance.objects.filter(date=date, attendee_type='staff', status='absent').count(),
        }
    
    context = {
        'attendance_summary': attendance_summary,
        'attendance_data': attendance_data,
    }
    return render(request, 'AdminApp/attendance.html', context)

@login_required
@user_passes_test(is_admin)
def events(request):
    events = Event.objects.all().order_by('-date')
    notices = Notice.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'event_form' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.created_by = request.user
                event.save()
                messages.success(request, 'Event created successfully!')
                return redirect('admin_events')
        elif 'notice_form' in request.POST:
            notice_form = NoticeForm(request.POST)
            if notice_form.is_valid():
                notice = notice_form.save(commit=False)
                notice.created_by = request.user
                notice.save()
                messages.success(request, 'Notice posted successfully!')
                return redirect('admin_events')
    else:
        event_form = EventForm()
        notice_form = NoticeForm()
    
    context = {
        'events': events,
        'notices': notices,
        'event_form': event_form,
        'notice_form': notice_form,
    }
    return render(request, 'AdminApp/events.html', context)

@login_required
@user_passes_test(is_admin)
def accounts(request):
    # Financial data
    transactions = Transaction.objects.all().order_by('-created_at')
    
    # Summary data
    total_earnings = Transaction.objects.filter(transaction_type__in=['fee', 'purchase']).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Unpaid fees
    unpaid_fees = Enrollment.objects.filter(fee_paid=False)
    
    context = {
        'transactions': transactions,
        'total_earnings': total_earnings,
        'total_expenses': total_expenses,
        'unpaid_fees': unpaid_fees,
    }
    return render(request, 'AdminApp/accounts.html', context)

@login_required
@user_passes_test(is_admin)
def reports(request):
    # This would generate reports for download
    # For now, just showing the page
    return render(request, 'AdminApp/reports.html')

class EmployeeCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
    ]
    SUBROLE_CHOICES = [
        ('faculty', 'Faculty'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('it', 'IT'),
        ('teacher', 'Teacher'),
        ('other', 'Other'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='employee')
    sub_role = forms.ChoiceField(choices=SUBROLE_CHOICES)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'sub_role', 'password1', 'password2')

class AdminCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

@login_required
@user_passes_test(is_admin)
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Employee account created successfully for {user.username}!')
            return redirect('admin_users')
    else:
        form = EmployeeCreationForm()
    
    return render(request, 'AdminApp/create_employee.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def create_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Admin account created successfully for {user.username}!')
            return redirect('admin_users')
    else:
        form = AdminCreationForm()
    
    return render(request, 'AdminApp/create_admin.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def users(request):
    users = User.objects.all().order_by('role', 'sub_role', 'username')
    context = {'users': users}
    return render(request, 'AdminApp/users.html', context)