from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from AuthApp.models import User, ActivityLog
from EmployeeApp.models import Course, ClassRoutine, Attendance
from AdminApp.models import Notice, Event, WeekendCalendar
from StudentApp.models import Enrollment, ExamResult, Certificate, FeePayment
from .forms import EnrollmentForm, CertificateApplicationForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required


# this two need for all views
# from django.utils import timezone
# from datetime import timedelta

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'StudentApp/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Summary Data
        active_enrollments = Enrollment.objects.filter(
            student=user, 
            status__in=['ongoing', 'approved']
        ).count()
        
        attendance_records = Attendance.objects.filter(user=user)
        total_classes = attendance_records.count()
        present_days = attendance_records.filter(status='present').count()
        attendance_rate = (present_days / total_classes * 100) if total_classes > 0 else 0
        
        certificates_earned = Certificate.objects.filter(
            student=user, 
            status='issued'
        ).count()
        
        unpaid_fees = FeePayment.objects.filter(
            enrollment__student=user,
            status__in=['pending', 'overdue']
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        context['summary_data'] = {
            'active_courses': active_enrollments,
            'attendance_rate': round(attendance_rate, 1),
            'certificates_earned': certificates_earned,
            'unpaid_fees': unpaid_fees,
        }
        
        # Upcoming Classes
        today = timezone.now().date()
        end_date = today + timedelta(days=7)
        
        enrolled_courses = Enrollment.objects.filter(
            student=user,
            status__in=['ongoing', 'approved']
        ).values_list('course', flat=True)
        
        upcoming_classes = ClassRoutine.objects.filter(
            course__in=enrolled_courses,
            is_active=True
        ).select_related('course')
        
        # Convert day of week to actual dates in the next 7 days
        day_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        upcoming_class_list = []
        for routine in upcoming_classes:
            weekday = day_map[routine.day_of_week]
            days_ahead = weekday - today.weekday()
            if days_ahead < 0:  # Target day already happened this week
                days_ahead += 7
            class_date = today + timedelta(days=days_ahead)
            
            if class_date <= end_date:
                upcoming_class_list.append({
                    'course': routine.course,
                    'date': class_date,
                    'start_time': routine.start_time,
                    'end_time': routine.end_time,
                    'room': routine.room,
                })
        
        context['upcoming_classes'] = sorted(upcoming_class_list, key=lambda x: (x['date'], x['start_time']))
        
        # Recent Results
        context['recent_results'] = ExamResult.objects.filter(
            enrollment__student=user
        ).order_by('-created_at')
        
        # My Courses
        context['my_courses'] = Enrollment.objects.filter(
            student=user,
            status__in=['ongoing', 'approved']
        ).select_related('course')
        
        # Calendar Data
        current_year = today.year
        current_month = today.month
        cal = calendar.monthcalendar(current_year, current_month)
        
        weekends = WeekendCalendar.objects.filter(
            date__year=current_year,
            date__month=current_month,
            is_weekend=True
        ).values_list('date', flat=True)
        
        context['calendar_data'] = {
            'year': current_year,
            'month': current_month,
            'month_name': calendar.month_name[current_month],
            'calendar': cal,
            'weekends': weekends,
        }
        
        # Academics Data
        exam_results = ExamResult.objects.filter(enrollment__student=user)
        total_exams = exam_results.count()
        passed_exams = exam_results.filter(passed=True).count()
        pass_rate = (passed_exams / total_exams * 100) if total_exams > 0 else 0
        
        context['academics_data'] = {
            'pass_rate': round(pass_rate, 1),
            'total_classes': total_classes,
            'achievements': certificates_earned,
        }
        
        # Attendance Records
        context['attendance_records'] = attendance_records
        
        # Notices
        context['notices'] = Notice.objects.filter(
            is_active=True
        ).order_by('-created_at')
        
        # Certificates
        context['earned_certificates'] = Certificate.objects.filter(
            student=user,
            status='issued'
        )
        
        context['pending_certificates'] = Certificate.objects.filter(
            student=user,
            status__in=['pending', 'approved']
        )
        
        # Available Courses
        context['available_courses'] = Course.objects.filter(
            status='active'
        ).exclude(
            id__in=Enrollment.objects.filter(
                student=user,
                status__in=['ongoing', 'approved']
            ).values_list('course', flat=True)
        )

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
        
        return context

class EnrollCourseView(LoginRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'student/enroll_form.html'
    success_url = reverse_lazy('student:dashboard')
    
    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.status = 'pending'
        return super().form_valid(form)

class ApplyCertificateView(LoginRequiredMixin, CreateView):
    model = Certificate
    form_class = CertificateApplicationForm
    template_name = 'student/apply_certificate.html'
    success_url = reverse_lazy('student:dashboard')
    
    def form_valid(self, form):
        enrollment_id = self.request.POST.get('enrollment')
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=self.request.user)
        form.instance.student = self.request.user
        form.instance.course = enrollment.course
        form.instance.status = 'pending'
        return super().form_valid(form)
    

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, f'You are already enrolled in {course.title}!')
        return redirect('student:dashboard')
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', '')
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course,
            status='pending'  # Default status as per your model
        )
        
        messages.success(request, 
            f'Your enrollment in {course.title} has been submitted! '
            f'Status: {enrollment.get_status_display()}. '
            f'Please wait for approval.')

        return redirect('student:dashboard')

    # For GET requests, redirect to dashboard
    return redirect('student:dashboard')

@login_required
def enrollment_details(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    
    return render(request, 'enrollment_details.html', {
        'enrollment': enrollment
    })

@login_required
def make_payment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    
    if enrollment.fee_paid:
        messages.warning(request, 'Fee for this enrollment has already been paid.')
        return redirect('student:dashboard')
    
    if request.method == 'POST':
        # Process payment (in a real app, you would integrate with a payment gateway)
        enrollment.fee_paid = True
        enrollment.save()
        
        messages.success(request, f'Payment for {enrollment.course.title} has been successfully processed!')
        return redirect('student:dashboard')
    
    return render(request, 'payment_form.html', {
        'enrollment': enrollment
    })