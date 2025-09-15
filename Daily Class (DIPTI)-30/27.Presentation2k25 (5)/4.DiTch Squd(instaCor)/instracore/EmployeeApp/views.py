# EmployeeApp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import datetime, timedelta
import calendar
import csv
import json

from .models import JobPost, Application, InterviewSchedule, Course, CourseTeacher, Assignment, LessonPlan, ClassRoutine, Attendance
from AuthApp.models import User, ActivityLog
from .forms import (
    UserCreationForm, UserUpdateForm, JobPostForm, ApplicationForm, InterviewScheduleForm,
    CourseForm, CourseTeacherForm, AssignmentForm, LessonPlanForm, ClassRoutineForm, AttendanceForm,
    UserFilterForm, JobPostFilterForm, ApplicationFilterForm, InterviewFilterForm, CourseFilterForm,
    AssignmentFilterForm, LessonPlanFilterForm, ClassRoutineFilterForm, AttendanceFilterForm
)

from AdminApp.models import Event, Notice

from django.core.paginator import Paginator
from StudentApp.models import Enrollment

# this two need for all views
# from django.utils import timezone
# from datetime import timedelta

# Helper functions for role checking
def is_hr(user):
    return user.is_authenticated and user.role == 'employee' and user.sub_role == 'hr'

def is_faculty(user):
    return user.is_authenticated and user.role == 'employee' and user.sub_role == 'faculty'

def is_teacher(user):
    return user.is_authenticated and user.role == 'employee' and user.sub_role == 'teacher'

# Dashboard views
@login_required
@user_passes_test(is_hr)
def hr_dashboard(request):
    # Summary data
    total_employees = User.objects.filter(role='employee').count()
    active_job_posts = JobPost.objects.filter(is_active=True).count()
    total_applications = Application.objects.count()
    scheduled_interviews = InterviewSchedule.objects.filter(status='scheduled').count()
    
    # Recent activities
    recent_activities = User.objects.filter(role='employee').order_by('-date_joined')[:5]
    
    # Upcoming interviews
    upcoming_interviews = InterviewSchedule.objects.filter(
        scheduled_date__gte=timezone.now(),
        status='scheduled'
    ).order_by('scheduled_date')[:5]
    
    # All data for modals
    users = User.objects.filter(Q(role='employee') | Q(role='candidate'))
    job_posts = JobPost.objects.all()
    applications = Application.objects.all()
    interviews = InterviewSchedule.objects.all()
    
    # Calendar data
    current_month = timezone.now().month
    current_year = timezone.now().year
    cal = calendar.monthcalendar(current_year, current_month)
    
    # Get weekends
    weekends = []
    for week in cal:
        for day in week:
            if day != 0:  # Skip empty days
                date_obj = datetime(current_year, current_month, day).date()
                # Friday is weekend (5 = Friday)
                if date_obj.weekday() == 5:  # 5 is Friday
                    weekends.append(day)
    
    context = {
        'summary_data': {
            'employees': {'total': total_employees, 'active': total_employees},
            'job_posts': {'total': active_job_posts, 'active': active_job_posts},
            'applications': {'total': total_applications, 'active': total_applications},
            'interviews': {'total': scheduled_interviews, 'active': scheduled_interviews},
        },
        'recent_activities': recent_activities,
        'upcoming_interviews': upcoming_interviews,
        'calendar_data': {
            'month_name': calendar.month_name[current_month],
            'year': current_year,
            'calendar': cal,
            'weekends': weekends,
        },
        'users': users,
        'job_posts': job_posts,
        'applications': applications,
        'interviews': interviews,
    }
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
    
    return render(request, 'EmployeeApp/hr_dashboard.html', context)

@login_required
@user_passes_test(is_faculty)
def faculty_dashboard(request):
    # Summary data
    total_teachers = User.objects.filter(role='employee', sub_role='teacher').count()
    total_students = User.objects.filter(role='student').count()
    active_courses = Course.objects.filter(status='active').count()
    pending_requests = Course.objects.filter(status='pending_approval').count()
    
    # Recent activities
    recent_activities = User.objects.filter(role='employee', sub_role='teacher').order_by('-date_joined')[:5]
    
    # Pending requests
    pending_course_requests = Course.objects.filter(status='pending_approval')[:5]
    
    # All data for modals
    courses = Course.objects.all()
    teachers = User.objects.filter(role='employee', sub_role='teacher')
    students = User.objects.filter(role='student')
    
    # Calendar data
    current_month = timezone.now().month
    current_year = timezone.now().year
    cal = calendar.monthcalendar(current_year, current_month)
    
    # Get weekends
    weekends = []
    for week in cal:
        for day in week:
            if day != 0:  # Skip empty days
                date_obj = datetime(current_year, current_month, day).date()
                # Friday is weekend (5 = Friday)
                if date_obj.weekday() == 5:  # 5 is Friday
                    weekends.append(day)
    
    context = {
        'summary_data': {
            'teachers': {'total': total_teachers, 'active': total_teachers},
            'students': {'total': total_students, 'active': total_students},
            'courses': {'total': active_courses, 'active': active_courses},
            'requests': {'total': pending_requests, 'active': pending_requests},
        },
        'recent_activities': recent_activities,
        'pending_requests': pending_course_requests,
        'calendar_data': {
            'month_name': calendar.month_name[current_month],
            'year': current_year,
            'calendar': cal,
            'weekends': weekends,
        },
        'courses': courses,
        'teachers': teachers,
        'students': students,
    }
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

    enrollments = Enrollment.objects.filter(status='pending')
    context.update({
        'enrollments': enrollments
    })

    return render(request, 'EmployeeApp/faculty_dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    # Get current teacher
    teacher = request.user
    
    # Summary data
    active_courses = Course.objects.filter(
        teachers__teacher=teacher,
        status='active'
    ).count()
    
    total_students = User.objects.filter(
        role='student',
        enrollments__course__teachers__teacher=teacher
    ).distinct().count()
    
    pending_tasks = Assignment.objects.filter(
        course__teachers__teacher=teacher,
        due_date__gte=timezone.now()
    ).count()
    
    # Get classes this week
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    classes_this_week = ClassRoutine.objects.filter(
        teacher=teacher,
        is_active=True
    ).count()
    
    # Recent activities
    recent_activities = Assignment.objects.filter(
        course__teachers__teacher=teacher
    ).order_by('-created_at')[:5]
    
    # Pending tasks
    pending_assignments = Assignment.objects.filter(
        course__teachers__teacher=teacher,
        due_date__gte=timezone.now()
    ).order_by('due_date')[:5]
    
    # All data for modals
    courses = Course.objects.filter(teachers__teacher=teacher)
    assignments = Assignment.objects.filter(course__teachers__teacher=teacher)
    lesson_plans = LessonPlan.objects.filter(course__teachers__teacher=teacher)
    class_routines = ClassRoutine.objects.filter(teacher=teacher)
    attendance_records = Attendance.objects.filter(
        user__enrollments__course__teachers__teacher=teacher
    )
    
    # Get students for attendance marking
    from StudentApp.models import Enrollment
    student_ids = Enrollment.objects.filter(
        course__teachers__teacher=teacher
    ).values_list('student_id', flat=True)
    students = User.objects.filter(id__in=student_ids)
    
    # Calendar data
    current_month = timezone.now().month
    current_year = timezone.now().year
    cal = calendar.monthcalendar(current_year, current_month)
    
    # Get weekends
    weekends = []
    for week in cal:
        for day in week:
            if day != 0:  # Skip empty days
                date_obj = datetime(current_year, current_month, day).date()
                # Friday is weekend (5 = Friday)
                if date_obj.weekday() == 5:  # 5 is Friday
                    weekends.append(day)
    
    context = {
        'summary_data': {
            'courses': {'total': active_courses, 'active': active_courses},
            'students': {'total': total_students, 'active': total_students},
            'tasks': {'total': pending_tasks, 'active': pending_tasks},
            'classes': {'total': classes_this_week, 'active': classes_this_week},
        },
        'recent_activities': recent_activities,
        'pending_tasks': pending_assignments,
        'calendar_data': {
            'month_name': calendar.month_name[current_month],
            'year': current_year,
            'calendar': cal,
            'weekends': weekends,
        },
        'courses': courses,
        'assignments': assignments,
        'lesson_plans': lesson_plans,
        'class_routines': class_routines,
        'attendance_records': attendance_records,
        'students': students,
    }
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
    return render(request, 'EmployeeApp/teacher_dashboard.html', context)

# User Management Views
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'EmployeeApp/faculty_dashboard.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def test_func(self):
        return is_hr(self.request.user) or is_faculty(self.request.user)
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # HR can see all employees but not admins or students
        if is_hr(self.request.user):
            queryset = queryset.filter(Q(role='employee') | Q(role='candidate'))
        
        # Faculty can see teachers and students
        if is_faculty(self.request.user):
            queryset = queryset.filter(Q(role='employee', sub_role='teacher') | Q(role='student'))
        
        # Apply filters
        form = UserFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['role']:
                queryset = queryset.filter(role=form.cleaned_data['role'])
            if form.cleaned_data['sub_role']:
                queryset = queryset.filter(sub_role=form.cleaned_data['sub_role'])
            if form.cleaned_data['search']:
                queryset = queryset.filter(
                    Q(username__icontains=form.cleaned_data['search']) |
                    Q(email__icontains=form.cleaned_data['search']) |
                    Q(first_name__icontains=form.cleaned_data['search']) |
                    Q(last_name__icontains=form.cleaned_data['search'])
                )
        
        return queryset.order_by('-date_joined')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = UserFilterForm(self.request.GET)
        return context

class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'EmployeeApp/user_detail.html'
    context_object_name = 'user_obj'
    
    def test_func(self):
        return is_hr(self.request.user) or is_faculty(self.request.user)

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'EmployeeApp/user_form.html'
    success_url = reverse_lazy('employee:user_list')
    
    def test_func(self):
        return is_hr(self.request.user) or is_faculty(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User created successfully.')
        return response

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'EmployeeApp/user_form.html'
    success_url = reverse_lazy('employee:user_list')
    
    def test_func(self):
        return is_hr(self.request.user) or is_faculty(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User updated successfully.')
        return response

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'EmployeeApp/user_confirm_delete.html'
    success_url = reverse_lazy('employee:user_list')
    
    def test_func(self):
        return is_hr(self.request.user) or is_faculty(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'User deleted successfully.')
        return response

# Job Post Views
class JobPostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = JobPost
    template_name = 'EmployeeApp/jobpost_list.html'
    context_object_name = 'job_posts'
    paginate_by = 10
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def get_queryset(self):
        queryset = JobPost.objects.all()
        
        # Apply filters
        form = JobPostFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['search']:
                queryset = queryset.filter(
                    Q(title__icontains=form.cleaned_data['search']) |
                    Q(description__icontains=form.cleaned_data['search'])
                )
            if form.cleaned_data['is_active']:
                queryset = queryset.filter(is_active=form.cleaned_data['is_active'] == '1')
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = JobPostFilterForm(self.request.GET)
        return context

class JobPostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = JobPost
    template_name = 'EmployeeApp/jobpost_detail.html'
    context_object_name = 'job_post'
    
    def test_func(self):
        return is_hr(self.request.user)

class JobPostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'EmployeeApp/jobpost_form.html'
    success_url = reverse_lazy('employee:jobpost_list')
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Job post created successfully.')
        return response

class JobPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'EmployeeApp/jobpost_form.html'
    success_url = reverse_lazy('employee:jobpost_list')
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Job post updated successfully.')
        return response

class JobPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobPost
    template_name = 'EmployeeApp/jobpost_confirm_delete.html'
    success_url = reverse_lazy('employee:jobpost_list')
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Job post deleted successfully.')
        return response

# Application Views
class ApplicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'EmployeeApp/application_list.html'
    context_object_name = 'applications'
    paginate_by = 10
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def get_queryset(self):
        queryset = Application.objects.all()
        
        # Apply filters
        form = ApplicationFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['job']:
                queryset = queryset.filter(job=form.cleaned_data['job'])
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
        
        return queryset.order_by('-applied_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ApplicationFilterForm(self.request.GET)
        return context

class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'EmployeeApp/application_detail.html'
    context_object_name = 'application'
    
    def test_func(self):
        return is_hr(self.request.user)

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'EmployeeApp/application_form.html'
    success_url = reverse_lazy('employee:application_list')
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Application updated successfully.')
        return response

# Interview Views
class InterviewListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = InterviewSchedule
    template_name = 'EmployeeApp/interview_list.html'
    context_object_name = 'interviews'
    paginate_by = 10
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def get_queryset(self):
        queryset = InterviewSchedule.objects.all()
        
        # Apply filters
        form = InterviewFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['search']:
                queryset = queryset.filter(
                    Q(application__applicant_name__icontains=form.cleaned_data['search']) |
                    Q(application__job__title__icontains=form.cleaned_data['search'])
                )
        
        return queryset.order_by('scheduled_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = InterviewFilterForm(self.request.GET)
        return context

class InterviewDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = InterviewSchedule
    template_name = 'EmployeeApp/interview_detail.html'
    context_object_name = 'interview'
    
    def test_func(self):
        return is_hr(self.request.user)

class InterviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = InterviewSchedule
    form_class = InterviewScheduleForm
    template_name = 'EmployeeApp/interview_form.html'
    success_url = reverse_lazy('employee:interview_list')
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def get_initial(self):
        initial = super().get_initial()
        application_id = self.request.GET.get('application_id')
        if application_id:
            application = get_object_or_404(Application, id=application_id)
            initial['application'] = application
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Interview scheduled successfully.')
        return response

class InterviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = InterviewSchedule
    form_class = InterviewScheduleForm
    template_name = 'EmployeeApp/interview_form.html'
    success_url = reverse_lazy('employee:interview_list')
    
    def test_func(self):
        return is_hr(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Interview updated successfully.')
        return response

# Course Views
class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = 'EmployeeApp/faculty_dashboard.html'
    context_object_name = 'courses'
    paginate_by = 10
    
    def test_func(self):
        return is_faculty(self.request.user) or is_teacher(self.request.user)
    
    def get_queryset(self):
        queryset = Course.objects.all()
        
        # Teachers can only see their own courses
        if is_teacher(self.request.user):
            queryset = queryset.filter(teachers__teacher=self.request.user)
        
        # Apply filters
        form = CourseFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['course_type']:
                queryset = queryset.filter(course_type=form.cleaned_data['course_type'])
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['search']:
                queryset = queryset.filter(
                    Q(title__icontains=form.cleaned_data['search']) |
                    Q(description__icontains=form.cleaned_data['search'])
                )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CourseFilterForm(self.request.GET)
        return context

class CourseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Course
    template_name = 'EmployeeApp/course_detail.html'
    context_object_name = 'course'
    
    def test_func(self):
        return is_faculty(self.request.user) or (
            is_teacher(self.request.user) and 
            Course.objects.filter(
                id=self.kwargs['pk'],
                teachers__teacher=self.request.user
            ).exists()
        )

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'EmployeeApp/course_form.html'
    
    def test_func(self):
        return is_faculty(self.request.user) or is_teacher(self.request.user)
    
    def get_success_url(self):
        if is_teacher(self.request.user):
            return reverse_lazy('employee:teacher_dashboard')
        return reverse_lazy('employee:course_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Teachers' courses need approval
        if is_teacher(self.request.user):
            form.instance.status = 'pending_approval'
            
        response = super().form_valid(form)
        messages.success(self.request, 'Course created successfully.')
        
        # If teacher created, add them as a teacher
        if is_teacher(self.request.user):
            CourseTeacher.objects.create(
                course=self.object,
                teacher=self.request.user,
                is_primary=True,
                assigned_by=self.request.user
            )
            
        return response

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'EmployeeApp/course_form.html'
    
    def test_func(self):
        return is_faculty(self.request.user) or (
            is_teacher(self.request.user) and 
            Course.objects.filter(
                id=self.kwargs['pk'],
                teachers__teacher=self.request.user
            ).exists()
        )
    
    def get_success_url(self):
        if is_teacher(self.request.user):
            return reverse_lazy('employee:teacher_dashboard')
        return reverse_lazy('employee:course_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Course updated successfully.')
        return response

class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'EmployeeApp/course_confirm_delete.html'
    
    def test_func(self):
        return is_faculty(self.request.user) or (
            is_teacher(self.request.user) and 
            Course.objects.filter(
                id=self.kwargs['pk'],
                teachers__teacher=self.request.user
            ).exists()
        )
    
    def get_success_url(self):
        if is_teacher(self.request.user):
            return reverse_lazy('employee:teacher_dashboard')
        return reverse_lazy('employee:course_list')
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Course deleted successfully.')
        return response

# Course Teacher Views
class CourseTeacherListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CourseTeacher
    template_name = 'EmployeeApp/faculty_dashboard.html'
    context_object_name = 'course_teachers'
    paginate_by = 10
    
    def test_func(self):
        return is_faculty(self.request.user)
    
    def get_queryset(self):
        return CourseTeacher.objects.all().order_by('-assigned_at')

class CourseTeacherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CourseTeacher
    form_class = CourseTeacherForm
    template_name = 'EmployeeApp/faculty_dashboard.html'
    success_url = reverse_lazy('employee:courseteacher_list')
    
    def test_func(self):
        return is_faculty(self.request.user)
    
    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Teacher assigned to course successfully.')
        return response

class CourseTeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CourseTeacher
    form_class = CourseTeacherForm
    template_name = 'EmployeeApp/courseteacher_form.html'
    success_url = reverse_lazy('employee:courseteacher_list')
    
    def test_func(self):
        return is_faculty(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Course teacher assignment updated successfully.')
        return response

class CourseTeacherDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CourseTeacher
    template_name = 'EmployeeApp/courseteacher_confirm_delete.html'
    success_url = reverse_lazy('employee:courseteacher_list')
    
    def test_func(self):
        return is_faculty(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Teacher removed from course successfully.')
        return response

# Assignment Views
class AssignmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Assignment
    template_name = 'EmployeeApp/teacher_dashboard.html'
    context_object_name = 'assignments'
    paginate_by = 10
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_queryset(self):
        # Teachers can only see assignments for their courses
        queryset = Assignment.objects.filter(
            course__teachers__teacher=self.request.user
        )
        
        # Apply filters
        form = AssignmentFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['course']:
                queryset = queryset.filter(course=form.cleaned_data['course'])
            if form.cleaned_data['is_active']:
                queryset = queryset.filter(is_active=form.cleaned_data['is_active'] == '1')
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AssignmentFilterForm(self.request.GET)
        return context

class AssignmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Assignment
    template_name = 'EmployeeApp/assignment_detail.html'
    context_object_name = 'assignment'
    
    def test_func(self):
        return is_teacher(self.request.user) and Assignment.objects.filter(
            id=self.kwargs['pk'],
            course__teachers__teacher=self.request.user
        ).exists()

class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'EmployeeApp/assignment_form.html'
    success_url = reverse_lazy('employee:assignment_list')
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Assignment created successfully.')
        return response

class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'EmployeeApp/assignment_form.html'
    success_url = reverse_lazy('employee:assignment_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and Assignment.objects.filter(
            id=self.kwargs['pk'],
            course__teachers__teacher=self.request.user
        ).exists()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Assignment updated successfully.')
        return response

class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    template_name = 'EmployeeApp/assignment_confirm_delete.html'
    success_url = reverse_lazy('employee:assignment_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and Assignment.objects.filter(
            id=self.kwargs['pk'],
            course__teachers__teacher=self.request.user
        ).exists()
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Assignment deleted successfully.')
        return response

# Lesson Plan Views
class LessonPlanListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LessonPlan
    template_name = 'EmployeeApp/teacher_dashboard.html'
    context_object_name = 'lesson_plans'
    paginate_by = 10
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_queryset(self):
        # Teachers can only see lesson plans for their courses
        queryset = LessonPlan.objects.filter(
            course__teachers__teacher=self.request.user
        )
        
        # Apply filters
        form = LessonPlanFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['course']:
                queryset = queryset.filter(course=form.cleaned_data['course'])
            if form.cleaned_data['month']:
                queryset = queryset.filter(date__month=form.cleaned_data['month'].month, 
                                          date__year=form.cleaned_data['month'].year)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = LessonPlanFilterForm(self.request.GET)
        return context

class LessonPlanDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = LessonPlan
    template_name = 'EmployeeApp/lessonplan_detail.html'
    context_object_name = 'lesson_plan'
    
    def test_func(self):
        return is_teacher(self.request.user) and LessonPlan.objects.filter(
            id=self.kwargs['pk'],
            course__teachers__teacher=self.request.user
        ).exists()

class LessonPlanCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = 'EmployeeApp/lessonplan_form.html'
    success_url = reverse_lazy('employee:lessonplan_list')
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Lesson plan created successfully.')
        return response

class LessonPlanUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = 'EmployeeApp/lessonplan_form.html'
    success_url = reverse_lazy('employee:lessonplan_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and LessonPlan.objects.filter(
            id=self.kwargs['pk'],
            course__teachers__teacher=self.request.user
        ).exists()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lesson plan updated successfully.')
        return response

class LessonPlanDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LessonPlan
    template_name = 'EmployeeApp/lessonplan_confirm_delete.html'
    success_url = reverse_lazy('employee:lessonplan_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and LessonPlan.objects.filter(
            id=self.kwargs['pk'],
            course__teachers__teacher=self.request.user
        ).exists()
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Lesson plan deleted successfully.')
        return response

# Class Routine Views
class ClassRoutineListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ClassRoutine
    template_name = 'EmployeeApp/teacher_dashboard.html'
    context_object_name = 'class_routines'
    paginate_by = 10
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_queryset(self):
        # Teachers can only see their own class routines
        queryset = ClassRoutine.objects.filter(
            teacher=self.request.user
        )
        
        # Apply filters
        form = ClassRoutineFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['course']:
                queryset = queryset.filter(course=form.cleaned_data['course'])
            if form.cleaned_data['day_of_week']:
                queryset = queryset.filter(day_of_week=form.cleaned_data['day_of_week'])
        
        return queryset.order_by('day_of_week', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ClassRoutineFilterForm(self.request.GET)
        return context

class ClassRoutineDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClassRoutine
    template_name = 'EmployeeApp/classroutine_detail.html'
    context_object_name = 'class_routine'
    
    def test_func(self):
        return is_teacher(self.request.user) and ClassRoutine.objects.filter(
            id=self.kwargs['pk'],
            teacher=self.request.user
        ).exists()

class ClassRoutineCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClassRoutine
    form_class = ClassRoutineForm
    template_name = 'EmployeeApp/classroutine_form.html'
    success_url = reverse_lazy('employee:classroutine_list')
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Class routine created successfully.')
        return response

class ClassRoutineUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClassRoutine
    form_class = ClassRoutineForm
    template_name = 'EmployeeApp/classroutine_form.html'
    success_url = reverse_lazy('employee:classroutine_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and ClassRoutine.objects.filter(
            id=self.kwargs['pk'],
            teacher=self.request.user
        ).exists()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Class routine updated successfully.')
        return response

class ClassRoutineDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClassRoutine
    template_name = 'EmployeeApp/classroutine_confirm_delete.html'
    success_url = reverse_lazy('employee:classroutine_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and ClassRoutine.objects.filter(
            id=self.kwargs['pk'],
            teacher=self.request.user
        ).exists()
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Class routine deleted successfully.')
        return response

# Attendance Views
class AttendanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Attendance
    template_name = 'EmployeeApp/teacher_dashboard.html'
    context_object_name = 'attendance_records'
    paginate_by = 10
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_queryset(self):
        # Teachers can only see attendance for their courses
        queryset = Attendance.objects.filter(
            user__enrollments__course__teachers__teacher=self.request.user
        )
        
        # Apply filters
        form = AttendanceFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['course']:
                queryset = queryset.filter(user__enrollments__course=form.cleaned_data['course'])
            if form.cleaned_data['date']:
                queryset = queryset.filter(date=form.cleaned_data['date'])
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
        
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AttendanceFilterForm(self.request.GET)
        return context

class AttendanceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Attendance
    template_name = 'EmployeeApp/attendance_detail.html'
    context_object_name = 'attendance_record'
    
    def test_func(self):
        return is_teacher(self.request.user) and Attendance.objects.filter(
            id=self.kwargs['pk'],
            user__enrollments__course__teachers__teacher=self.request.user
        ).exists()

class AttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'EmployeeApp/attendance_form.html'
    success_url = reverse_lazy('employee:attendance_list')
    
    def test_func(self):
        return is_teacher(self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.marked_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Attendance marked successfully.')
        return response

class AttendanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'EmployeeApp/attendance_form.html'
    success_url = reverse_lazy('employee:attendance_list')
    
    def test_func(self):
        return is_teacher(self.request.user) and Attendance.objects.filter(
            id=self.kwargs['pk'],
            user__enrollments__course__teachers__teacher=self.request.user
        ).exists()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Attendance updated successfully.')
        return response

# Export Data Views
@login_required
@user_passes_test(lambda u: is_hr(u) or is_faculty(u))
def export_employee_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Role', 'Sub Role', 'Date of Birth', 'Phone', 'Gender', 'Location', 'Country', 'Is Active'])
    
    if is_hr(request.user):
        users = User.objects.filter(Q(role='employee') | Q(role='candidate'))
    else:  # Faculty
        users = User.objects.filter(Q(role='employee', sub_role='teacher') | Q(role='student'))
    
    for user in users:
        writer.writerow([
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.role,
            user.sub_role,
            user.date_of_birth,
            user.phone,
            user.gender,
            user.location,
            user.country,
            user.is_active
        ])
    
    return response

@login_required
@user_passes_test(is_hr)
def export_job_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_posts.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Role', 'Minimum Requirements', 'Salary Range', 'Location', 'Language', 'Availability', 'Application Instructions', 'Posted By', 'Created At', 'Deadline', 'Is Active'])
    
    job_posts = JobPost.objects.all()
    for job in job_posts:
        writer.writerow([
            job.title,
            job.description,
            job.role,
            job.min_requirements,
            job.salary_range,
            job.location,
            job.language,
            job.availability,
            job.application_instructions,
            job.posted_by.username if job.posted_by else '',
            job.created_at,
            job.deadline,
            job.is_active
        ])
    
    return response

@login_required
@user_passes_test(is_hr)
def export_application_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Job Title', 'Applicant Name', 'Applicant Email', 'Status', 'Applied At', 'Resume', 'Cover Letter'])
    
    applications = Application.objects.all()
    for app in applications:
        writer.writerow([
            app.job.title,
            app.applicant_name,
            app.applicant_email,
            app.status,
            app.applied_at,
            app.resume.url if app.resume else '',
            app.cover_letter
        ])
    
    return response

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_teacher(u))
def export_course_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Course Type', 'Price', 'Duration', 'Status', 'Created By', 'Created At'])
    
    if is_teacher(request.user):
        courses = Course.objects.filter(teachers__teacher=request.user)
    else:  # Faculty
        courses = Course.objects.all()
    
    for course in courses:
        writer.writerow([
            course.title,
            course.description,
            course.course_type,
            course.price,
            course.duration,
            course.status,
            course.created_by.username if course.created_by else '',
            course.created_at
        ])
    
    return response

@login_required
@user_passes_test(is_teacher)
def export_assignment_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assignments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Course', 'Description', 'Due Date', 'Total Marks', 'Is Active', 'Created By', 'Created At'])
    
    assignments = Assignment.objects.filter(course__teachers__teacher=request.user)
    for assignment in assignments:
        writer.writerow([
            assignment.title,
            assignment.course.title,
            assignment.description,
            assignment.due_date,
            assignment.total_marks,
            assignment.is_active,
            assignment.created_by.username if assignment.created_by else '',
            assignment.created_at
        ])
    
    return response

@login_required
@user_passes_test(is_teacher)
def export_lessonplan_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lesson_plans.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Course', 'Content', 'Date', 'Created By', 'Created At'])
    
    lesson_plans = LessonPlan.objects.filter(course__teachers__teacher=request.user)
    for lesson_plan in lesson_plans:
        writer.writerow([
            lesson_plan.title,
            lesson_plan.course.title,
            lesson_plan.content,
            lesson_plan.date,
            lesson_plan.created_by.username if lesson_plan.created_by else '',
            lesson_plan.created_at
        ])
    
    return response

@login_required
@user_passes_test(is_teacher)
def export_attendance_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student', 'Date', 'Status', 'Check In Time', 'Check Out Time', 'Notes', 'Marked By'])
    
    attendance_records = Attendance.objects.filter(
        user__enrollments__course__teachers__teacher=request.user
    )
    for record in attendance_records:
        writer.writerow([
            f"{record.user.first_name} {record.user.last_name}",
            record.date,
            record.status,
            record.check_in_time,
            record.check_out_time,
            record.notes,
            record.marked_by.username if record.marked_by else ''
        ])
    
    return response

# Chart data views
@login_required
@user_passes_test(is_hr)
def hr_chart_data(request):
    chart_type = request.GET.get('type')
    
    if chart_type == 'applications_by_job':
        # Get application counts by job post
        job_posts = JobPost.objects.annotate(
            application_count=Count('employee_applications')
        ).values('title', 'application_count')
        
        data = {
            'labels': [job['title'] for job in job_posts],
            'datasets': [{
                'label': 'Applications',
                'data': [job['application_count'] for job in job_posts],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        }
    elif chart_type == 'employee_distribution':
        # Get employee distribution by sub_role
        employees = User.objects.filter(role='employee').values('sub_role').annotate(
            count=Count('id')
        )
        
        data = {
            'labels': [emp['sub_role'] or 'Not specified' for emp in employees],
            'datasets': [{
                'data': [emp['count'] for emp in employees],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                'borderWidth': 1
            }]
        }
    else:
        data = {'error': 'Invalid chart type'}
    
    return JsonResponse(data)

@login_required
@user_passes_test(is_faculty)
def faculty_chart_data(request):
    chart_type = request.GET.get('type')
    
    if chart_type == 'course_enrollment':
        # Get course enrollment counts
        from StudentApp.models import Enrollment
        courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).values('title', 'enrollment_count')
        
        data = {
            'labels': [course['title'] for course in courses],
            'datasets': [{
                'label': 'Enrollments',
                'data': [course['enrollment_count'] for course in courses],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        }
    elif chart_type == 'course_distribution':
        # Get course distribution by type
        courses = Course.objects.values('course_type').annotate(
            count=Count('id')
        )
        
        data = {
            'labels': [course['course_type'] for course in courses],
            'datasets': [{
                'data': [course['count'] for course in courses],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                'borderWidth': 1
            }]
        }
    else:
        data = {'error': 'Invalid chart type'}
    
    return JsonResponse(data)

@login_required
@user_passes_test(is_teacher)
def teacher_chart_data(request):
    chart_type = request.GET.get('type')
    
    if chart_type == 'todays_schedule':
        # Get today's schedule
        today = timezone.now().date()
        weekday = today.strftime('%A').lower()
        
        routines = ClassRoutine.objects.filter(
            teacher=request.user,
            day_of_week=weekday,
            is_active=True
        ).order_by('start_time')
        
        data = {
            'labels': [f"{routine.start_time} - {routine.end_time}" for routine in routines],
            'datasets': [{
                'label': 'Today\'s Classes',
                'data': [1 for _ in routines],  # Just showing count
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 1
            }]
        }
    elif chart_type == 'attendance_summary':
        # Get attendance summary for the teacher's courses
        present_count = Attendance.objects.filter(
            user__enrollments__course__teachers__teacher=request.user,
            status='present'
        ).count()
        
        absent_count = Attendance.objects.filter(
            user__enrollments__course__teachers__teacher=request.user,
            status='absent'
        ).count()
        
        leave_count = Attendance.objects.filter(
            user__enrollments__course__teachers__teacher=request.user,
            status='leave'
        ).count()
        
        data = {
            'labels': ['Present', 'Absent', 'On Leave'],
            'datasets': [{
                'data': [present_count, absent_count, leave_count],
                'backgroundColor': [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                'borderColor': [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                'borderWidth': 1
            }]
        }
    else:
        data = {'error': 'Invalid chart type'}
    
    return JsonResponse(data)

@login_required
def pending_enrollments_table(request):
    pending_enrollments = Enrollment.objects.filter(status='pending').order_by('-enrolled_at')
    return render(request, 'pending_enrollments_table.html', {'enrollments': pending_enrollments})

@login_required
def enrollment_action(request, enrollment_id, action):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if action == 'accept':
        enrollment.status = 'approved'
    elif action == 'reject':
        enrollment.status = 'rejected'
    
    enrollment.save()
    return redirect('employee:faculty_dashboard')