from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from AuthApp.models import User
from .models import (
    JobPost, Application, InterviewSchedule, 
    Salary, Expense, Transaction, 
    Course, Assignment, LessonPlan, Attendance
)
from .forms import (
    JobPostForm, ApplicationForm, InterviewScheduleForm,
    SalaryForm, ExpenseForm, TransactionForm,
    CourseForm, AssignmentForm, LessonPlanForm, AttendanceForm
)

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'employee':
        if user.sub_role == 'faculty':
            return redirect('faculty_dashboard')
        elif user.sub_role == 'hr':
            return redirect('hr_dashboard')
        elif user.sub_role == 'finance':
            return redirect('finance_dashboard')
        elif user.sub_role == 'teacher':
            return redirect('teacher_dashboard')
        else:
            return redirect('other_dashboard')
    return redirect('login')

# Faculty Dashboard
@login_required
def faculty_dashboard(request):
    # Only faculty can access this
    if request.user.sub_role != 'faculty':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Summary data
    total_teachers = User.objects.filter(sub_role='teacher').count()
    active_teachers = User.objects.filter(sub_role='teacher', is_active=True).count()
    
    total_students = User.objects.filter(role='student').count()
    active_students = User.objects.filter(role='student', is_active=True).count()
    
    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(status='active').count()
    
    # Recent courses
    recent_courses = Course.objects.order_by('-created_at')[:5]
    
    # Pending requests
    pending_requests = Course.objects.filter(status='draft').count()
    
    context = {
        'total_teachers': total_teachers,
        'active_teachers': active_teachers,
        'total_students': total_students,
        'active_students': active_students,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'recent_courses': recent_courses,
        'pending_requests': pending_requests,
    }
    
    return render(request, 'EmployeeApp/faculty_dashboard.html', context)

# HR Dashboard
@login_required
def hr_dashboard(request):
    # Only HR can access this
    if request.user.sub_role != 'hr':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Summary data
    total_employees = User.objects.filter(role='employee').count()
    active_employees = User.objects.filter(role='employee', is_active=True).count()
    
    total_job_posts = JobPost.objects.count()
    active_job_posts = JobPost.objects.filter(is_active=True).count()
    
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='pending').count()
    
    # Recent job posts
    recent_job_posts = JobPost.objects.order_by('-created_at')[:5]
    
    # Recent applications
    recent_applications = Application.objects.order_by('-applied_at')[:5]
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'total_job_posts': total_job_posts,
        'active_job_posts': active_job_posts,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'recent_job_posts': recent_job_posts,
        'recent_applications': recent_applications,
    }
    
    return render(request, 'EmployeeApp/hr_dashboard.html', context)

# Finance Dashboard
@login_required
def finance_dashboard(request):
    # Only Finance can access this
    if request.user.sub_role != 'finance':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Summary data
    total_earnings = Transaction.objects.filter(
        transaction_type__in=['fee', 'purchase']
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    pending_salaries = Salary.objects.filter(status='pending').count()
    pending_expenses = Expense.objects.filter(is_approved=False).count()
    
    # Recent transactions
    recent_transactions = Transaction.objects.order_by('-created_at')[:10]
    
    # Monthly expense summary
    current_month = timezone.now().date().replace(day=1)
    monthly_expenses = Expense.objects.filter(date__gte=current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'total_earnings': total_earnings,
        'total_expenses': total_expenses,
        'pending_salaries': pending_salaries,
        'pending_expenses': pending_expenses,
        'recent_transactions': recent_transactions,
        'monthly_expenses': monthly_expenses,
    }
    
    return render(request, 'EmployeeApp/finance_dashboard.html', context)

# Teacher Dashboard
@login_required
def teacher_dashboard(request):
    # Only teachers can access this
    if request.user.sub_role != 'teacher':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Get courses assigned to this teacher
    assigned_courses = request.user.courses.all()
    
    # Summary data
    total_courses = assigned_courses.count()
    active_courses = assigned_courses.filter(status='active').count()
    
    # Total students in all courses
    from StudentApp.models import Enrollment
    total_students = Enrollment.objects.filter(course__in=assigned_courses).values('student').distinct().count()
    
    # Today's classes
    today = timezone.now().date()
    todays_classes = LessonPlan.objects.filter(
        course__in=assigned_courses,
        date=today
    ).order_by('date')
    
    # Upcoming assignments
    upcoming_assignments = Assignment.objects.filter(
        course__in=assigned_courses,
        due_date__gte=today
    ).order_by('due_date')[:5]
    
    # Recent attendance marked
    recent_attendance = Attendance.objects.filter(
        marked_by=request.user
    ).order_by('-marked_at')[:5]
    
    context = {
        'total_courses': total_courses,
        'active_courses': active_courses,
        'total_students': total_students,
        'todays_classes': todays_classes,
        'upcoming_assignments': upcoming_assignments,
        'recent_attendance': recent_attendance,
    }
    
    return render(request, 'EmployeeApp/teacher_dashboard.html', context)

# Other Dashboard (Librarian, Security, etc.)
@login_required
def other_dashboard(request):
    # For other employee roles
    if request.user.role != 'employee' or request.user.sub_role not in ['other']:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Basic dashboard for other roles
    context = {
        'user': request.user,
    }
    
    return render(request, 'EmployeeApp/other_dashboard.html', context)

# Course Management Views
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'EmployeeApp/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'EmployeeApp/course_form.html', {'form': form})

@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'EmployeeApp/course_form.html', {'form': form, 'course': course})

# Attendance Views
@login_required
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'EmployeeApp/attendance_list.html', {'attendances': attendances})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    
    return render(request, 'EmployeeApp/attendance_form.html', {'form': form})

# Job Post Views (HR)
@login_required
def job_post_list(request):
    if request.user.sub_role != 'hr':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    job_posts = JobPost.objects.all()
    return render(request, 'EmployeeApp/job_post_list.html', {'job_posts': job_posts})

@login_required
def job_post_create(request):
    if request.user.sub_role != 'hr':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.posted_by = request.user
            job_post.save()
            messages.success(request, 'Job post created successfully!')
            return redirect('job_post_list')
    else:
        form = JobPostForm()
    
    return render(request, 'EmployeeApp/job_post_form.html', {'form': form})

# Salary Views (Finance)
@login_required
def salary_list(request):
    if request.user.sub_role != 'finance':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    salaries = Salary.objects.all()
    return render(request, 'EmployeeApp/salary_list.html', {'salaries': salaries})

@login_required
def salary_create(request):
    if request.user.sub_role != 'finance':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save()
            messages.success(request, 'Salary record created successfully!')
            return redirect('salary_list')
    else:
        form = SalaryForm()
    
    return render(request, 'EmployeeApp/salary_form.html', {'form': form})

# Expense Views (Finance)
@login_required
def expense_list(request):
    if request.user.sub_role != 'finance':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    expenses = Expense.objects.all()
    return render(request, 'EmployeeApp/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.user.sub_role != 'finance':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.save()
            messages.success(request, 'Expense record created successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'EmployeeApp/expense_form.html', {'form': form})