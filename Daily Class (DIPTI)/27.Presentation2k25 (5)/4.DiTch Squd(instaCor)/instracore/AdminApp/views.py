from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import csv
from datetime import datetime, timedelta
from calendar import monthcalendar, month_name
from AuthApp.models import User, ActivityLog
from AdminApp.models import Event, Notice, WeekendCalendar, FinancialOverview
from EmployeeApp.models import Course, Attendance, Salary, Expense, Transaction
from StudentApp.models import Enrollment, FeePayment

from django.contrib.auth.hashers import make_password
from .forms import UserUpdateForm


# this two need for all views
# from django.utils import timezone
# from datetime import timedelta


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    users = User.objects.all()

    # Get summary data
    students = User.objects.filter(role='student')
    total_students = students.count()
    active_students = students.filter(is_active=True).count()
    
    teachers = User.objects.filter(Q(role='employee') & Q(sub_role__in=['faculty', 'teacher']))
    total_teachers = teachers.count()
    active_teachers = teachers.filter(is_active=True).count()
    
    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(status='active').count()
    
    staff = User.objects.filter(role='employee').exclude(sub_role__in=['faculty', 'teacher'])
    total_staff = staff.count()
    active_staff = staff.filter(is_active=True).count()
    
    summary_data = {
        'students': {
            'total': total_students,
            'active': active_students
        },
        'teachers': {
            'total': total_teachers,
            'active': active_teachers
        },
        'courses': {
            'total': total_courses,
            'active': active_courses
        },
        'staff': {
            'total': total_staff,
            'active': active_staff
        }
    }
    
    # Get attendance data (for current month)
    today = timezone.now().date()
    start_date = today.replace(day=1)
    if today.month == 12:
        end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    # Get student attendance
    students = User.objects.filter(role='student')
    student_attendance = Attendance.objects.filter(
        user__in=students,
        date__gte=start_date,
        date__lte=end_date
    )
    student_present = student_attendance.filter(status='present').count()
    student_absent = student_attendance.filter(status='absent').count()
    
    # Get teacher attendance
    teachers = User.objects.filter(Q(role='employee') & Q(sub_role__in=['faculty', 'teacher']))
    teacher_attendance = Attendance.objects.filter(
        user__in=teachers,
        date__gte=start_date,
        date__lte=end_date
    )
    teacher_present = teacher_attendance.filter(status='present').count()
    teacher_absent = teacher_attendance.filter(status='absent').count()
    
    # Get staff attendance
    staff = User.objects.filter(role='employee').exclude(sub_role__in=['faculty', 'teacher'])
    staff_attendance = Attendance.objects.filter(
        user__in=staff,
        date__gte=start_date,
        date__lte=end_date
    )
    staff_present = staff_attendance.filter(status='present').count()
    staff_absent = staff_attendance.filter(status='absent').count()
    
    attendance_data = {
        'students': {
            'present': student_present,
            'absent': student_absent
        },
        'teachers': {
            'present': teacher_present,
            'absent': teacher_absent
        },
        'staff': {
            'present': staff_present,
            'absent': staff_absent
        }
    }
    
    # Get course data
    courses = Course.objects.all()
    online_count = courses.filter(course_type='online').count()
    regular_count = courses.filter(course_type='regular').count()
    diploma_count = courses.filter(course_type='diploma').count()
    offline_count = courses.filter(course_type='offline').count()
    
    course_data = {
        'online': online_count,
        'regular': regular_count,
        'diploma': diploma_count,
        'offline': offline_count
    }
    
    # Get financial data
    current_month = timezone.now().replace(day=1)
    
    try:
        financial_data = FinancialOverview.objects.get(month=current_month)
        income = float(financial_data.income)
        expenses = float(financial_data.expenses)
        fees_collected = float(financial_data.fees_collected)
    except FinancialOverview.DoesNotExist:
        income = 0.0
        expenses = 0.0
        fees_collected = 0.0
    
    # Calculate unpaid fees
    unpaid_fees = float(FeePayment.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0)
    
    # Calculate net profit
    net_profit = income + fees_collected - expenses
    
    financial_data = {
        'income': income,
        'expenses': expenses,
        'fees_collected': fees_collected,
        'unpaid_fees': unpaid_fees,
        'net_profit': net_profit
    }
    
    # Get recent activities
    recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]
    
    # Get notices
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Get upcoming events
    events = Event.objects.filter(
        date__gte=today,
        is_active=True
    ).order_by('date')[:5]
    
    # Get current month name and year
    current_month = f"{month_name[today.month]} {today.year}"

    # Get all activities (not just recent ones)
    all_activities = ActivityLog.objects.order_by('-timestamp')
    
    # Get all notices (not just recent ones)
    all_notices = Notice.objects.filter(is_active=True).order_by('-created_at')
    
    # Get all events (not just upcoming ones)
    all_events = Event.objects.filter(is_active=True).order_by('-date')
    
    context = {
        'summary_data': summary_data,
        'attendance_data': attendance_data,
        'course_data': course_data,
        'financial_data': financial_data,
        'recent_activities': recent_activities[:10],  # Limit to 10
        'notices': notices[:5],  # Limit to 5
        'events': events[:5],  # Limit to 5
        'all_activities': all_activities,
        'all_notices': all_notices,
        'all_events': all_events,
        'current_month': current_month
    }

    context.update({
        "users": users,
        "all_activities": ActivityLog.objects.order_by("-timestamp"),
        "all_notices": Notice.objects.filter(is_active=True).order_by("-created_at"),
        "all_events": Event.objects.filter(is_active=True).order_by("-date"),
    })

    # this one need for all views
    # Recent activities in the last 15 minutes
    fifteen_minutes_ago = timezone.now() - timedelta(minutes=15)
    recent_activities_15min = ActivityLog.objects.filter(
        timestamp__gte=fifteen_minutes_ago
    ).order_by('-timestamp')

    # Notices (active)
    active_notices = Notice.objects.filter(is_active=True).order_by('-created_at')

    # Upcoming events
    upcoming_events = Event.objects.filter(
        is_active=True, date__gte=timezone.now().date()
    ).order_by('date')

    # Annotate type for template
    for notice in active_notices:
        notice.type = 'notice'
    for event in upcoming_events:
        event.type = 'event'
    for activity in recent_activities_15min:
        activity.type = 'activity'

    # Combine and sort by newest
    combined_notifications = list(active_notices) + list(upcoming_events) + list(recent_activities_15min)
    combined_notifications.sort(
        key=lambda x: getattr(x, 'created_at', getattr(x, 'date', getattr(x, 'timestamp', timezone.now()))),
        reverse=True
    )

    # Limit to last 6 notifications
    combined_notifications = combined_notifications[:6]

    context.update({
        'combined_notifications': combined_notifications
    })
    return render(request, 'AdminApp/dashboard.html', context)


# API endpoints for dashboard data
@login_required
@user_passes_test(is_admin)
def dashboard_attendance(request):
    period = request.GET.get('period', 'month')
    today = timezone.now().date()
    
    if period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:  # month
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    # Get student attendance
    students = User.objects.filter(role='student')
    student_attendance = Attendance.objects.filter(
        user__in=students,
        date__gte=start_date,
        date__lte=end_date
    )
    student_present = student_attendance.filter(status='present').count()
    student_absent = student_attendance.filter(status='absent').count()
    
    # Get teacher attendance
    teachers = User.objects.filter(Q(role='employee') & Q(sub_role__in=['faculty', 'teacher']))
    teacher_attendance = Attendance.objects.filter(
        user__in=teachers,
        date__gte=start_date,
        date__lte=end_date
    )
    teacher_present = teacher_attendance.filter(status='present').count()
    teacher_absent = teacher_attendance.filter(status='absent').count()
    
    # Get staff attendance
    staff = User.objects.filter(role='employee').exclude(sub_role__in=['faculty', 'teacher'])
    staff_attendance = Attendance.objects.filter(
        user__in=staff,
        date__gte=start_date,
        date__lte=end_date
    )
    staff_present = staff_attendance.filter(status='present').count()
    staff_absent = staff_attendance.filter(status='absent').count()
    
    return JsonResponse({
        'students': {
            'present': student_present,
            'absent': student_absent
        },
        'teachers': {
            'present': teacher_present,
            'absent': teacher_absent
        },
        'staff': {
            'present': staff_present,
            'absent': staff_absent
        }
    })


@login_required
@user_passes_test(is_admin)
def dashboard_courses(request):
    status = request.GET.get('status', 'all')
    
    if status == 'active':
        courses = Course.objects.filter(status='active')
    elif status == 'inactive':
        courses = Course.objects.exclude(status='active')
    else:  # all
        courses = Course.objects.all()
    
    online_count = courses.filter(course_type='online').count()
    regular_count = courses.filter(course_type='regular').count()
    diploma_count = courses.filter(course_type='diploma').count()
    offline_count = courses.filter(course_type='offline').count()
    
    return JsonResponse({
        'online': online_count,
        'regular': regular_count,
        'diploma': diploma_count,
        'offline': offline_count
    })


@login_required
@user_passes_test(is_admin)
def dashboard_weekend_days(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Get weekend days for the specified month
    weekend_days = WeekendCalendar.objects.filter(
        date__year=year,
        date__month=month
    )
    
    # If no weekend days are recorded, generate them for Bangladesh calendar
    if not weekend_days.exists():
        cal = monthcalendar(year, month)
        weekend_days_list = []
        
        # Bangladesh government holidays (example dates - you should update with actual holidays)
        bd_holidays = {
            # Fixed holidays
            (1, 1): "New Year's Day",
            (2, 21): "International Mother Language Day",
            (3, 26): "Independence Day",
            (4, 14): "Bengali New Year",
            (5, 1): "May Day",
            (8, 15): "National Mourning Day",
            (12, 16): "Victory Day",
            (12, 25): "Christmas Day",
            
            # Islamic holidays (approximate dates - these change every year based on lunar calendar)
            # You should update these with actual dates for each year
        }
        
        for week in cal:
            for day_idx, day in enumerate(week):
                if day == 0:  # Day not in this month
                    continue
                
                date = datetime(year, month, day).date()
                # In Bangladesh, Friday is the weekend (day_idx 5 in standard calendar)
                is_weekend = (day_idx == 5)  # Friday
                
                # Check if it's a government holiday
                is_holiday = (month, day) in bd_holidays
                description = ""
                
                if is_weekend:
                    description = "Weekend"
                elif is_holiday:
                    description = bd_holidays[(month, day)]
                else:
                    description = "Weekday"
                
                weekend_day = WeekendCalendar(
                    date=date,
                    is_weekend=is_weekend,
                    is_holiday=is_holiday,
                    description=description
                )
                weekend_day.save()
                weekend_days_list.append({
                    'date': date.isoformat(),
                    'is_weekend': is_weekend,
                    'is_holiday': is_holiday,
                    'description': description
                })
        
        return JsonResponse(weekend_days_list, safe=False)
    
    # Return existing weekend days
    weekend_days_list = []
    for day in weekend_days:
        weekend_days_list.append({
            'date': day.date.isoformat(),
            'is_weekend': day.is_weekend,
            'is_holiday': getattr(day, 'is_holiday', False),
            'description': day.description
        })
    
    return JsonResponse(weekend_days_list, safe=False)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_user(request):
    try:
        # Create new user
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            role=request.POST.get('role')
        )
        
        # Set sub_role if provided
        if request.POST.get('sub_role'):
            user.sub_role = request.POST.get('sub_role')
            user.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action=f"Created new {request.POST.get('role')} user: {user.username}"
        )
        
        messages.success(request, f"{request.POST.get('role').capitalize()} created successfully!")
        return redirect('admin_dashboard:dashboard')
    except Exception as e:
        messages.error(request, f"Error creating user: {str(e)}")
        return redirect('admin_dashboard:dashboard')


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_notice(request):
    try:
        # Create new notice
        notice = Notice.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            category=request.POST.get('category'),
            priority=request.POST.get('priority'),
            created_by=request.user
        )
        
        # Set expiry date if provided
        if request.POST.get('expiry_date'):
            notice.expiry_date = request.POST.get('expiry_date')
            notice.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action=f"Created new notice: {notice.title}"
        )
        
        messages.success(request, "Notice created successfully!")
        return redirect('admin_dashboard:dashboard')
    except Exception as e:
        messages.error(request, f"Error creating notice: {str(e)}")
        return redirect('admin_dashboard:dashboard')


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_event(request):
    try:
        # Create new event
        event = Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            date=request.POST.get('date'),
            created_by=request.user
        )
        
        # Set optional fields if provided
        if request.POST.get('start_time'):
            event.start_time = request.POST.get('start_time')
        
        if request.POST.get('end_time'):
            event.end_time = request.POST.get('end_time')
        
        if request.POST.get('location'):
            event.location = request.POST.get('location')
        
        event.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action=f"Created new event: {event.title}"
        )
        
        messages.success(request, "Event created successfully!")
        return redirect('admin_dashboard:dashboard')
    except Exception as e:
        messages.error(request, f"Error creating event: {str(e)}")
        return redirect('admin_dashboard:dashboard')


@login_required
@user_passes_test(is_admin)
def create_financial_data(request):
    if request.method == 'POST':
        try:
            current_month = timezone.now().replace(day=1)
            
            # Check if financial data already exists for this month
            financial_data, created = FinancialOverview.objects.get_or_create(
                month=current_month,
                defaults={
                    'income': 0,
                    'expenses': 0,
                    'fees_collected': 0,
                    'salaries_paid': 0
                }
            )
            
            # Update with form data
            financial_data.income = float(request.POST.get('income', 0))
            financial_data.expenses = float(request.POST.get('expenses', 0))
            financial_data.fees_collected = float(request.POST.get('fees_collected', 0))
            financial_data.salaries_paid = float(request.POST.get('salaries_paid', 0))
            financial_data.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action=f"Updated financial data for {current_month.strftime('%B %Y')}"
            )
            
            messages.success(request, "Financial data updated successfully!")
            return redirect('admin_dashboard:dashboard')
        except Exception as e:
            messages.error(request, f"Error updating financial data: {str(e)}")
            return redirect('admin_dashboard:create_financial_data')
    
    return render(request, 'create_financial_data.html')


@login_required
@user_passes_test(is_admin)
def export_data(request, data_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{data_type}_data_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    if data_type == 'student':
        # Export student data
        writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Phone', 'Location', 'Status'])
        
        students = User.objects.filter(role='student')
        for student in students:
            writer.writerow([
                student.username,
                student.first_name,
                student.last_name,
                student.email,
                student.phone,
                student.location,
                'Active' if student.is_active else 'Inactive'
            ])
    
    elif data_type == 'employee':
        # Export employee data
        writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Role', 'Sub Role', 'Phone', 'Status'])
        
        employees = User.objects.filter(role='employee')
        for employee in employees:
            writer.writerow([
                employee.username,
                employee.first_name,
                employee.last_name,
                employee.email,
                employee.role,
                employee.sub_role or '',
                employee.phone,
                'Active' if employee.is_active else 'Inactive'
            ])
    
    elif data_type == 'course':
        # Export course data
        writer.writerow(['Title', 'Type', 'Price', 'Duration', 'Status', 'Created By'])
        
        courses = Course.objects.all()
        for course in courses:
            writer.writerow([
                course.title,
                course.course_type,
                course.price,
                course.duration,
                course.status,
                course.created_by.username if course.created_by else ''
            ])
    
    elif data_type == 'account':
        # Export financial data
        writer.writerow(['Month', 'Income', 'Expenses', 'Fees Collected', 'Salaries Paid'])
        
        financial_data = FinancialOverview.objects.all().order_by('month')
        for data in financial_data:
            writer.writerow([
                data.month.strftime('%Y-%m'),
                data.income,
                data.expenses,
                data.fees_collected,
                data.salaries_paid
            ])
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action=f"Exported {data_type} data"
    )
    
    return response

@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            u = form.save(commit=False)
            pwd1 = request.POST.get("password1")
            pwd2 = request.POST.get("password2")
            if pwd1 and pwd1 == pwd2:
                u.password = make_password(pwd1)
            u.save()
            messages.success(request, "User updated successfully")
        else:
            messages.error(request, "Update failed")
    return redirect("admin_dashboard:dashboard")

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect("admin_dashboard:dashboard")