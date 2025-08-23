from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from AuthApp.models import User
from EmployeeApp.models import Course, Assignment, Attendance, LessonPlan
from .models import (
    Enrollment, ExamResult, Certificate, 
    GuardianReport, LeaveApplication, FeePayment
)
from .forms import (
    EnrollmentForm, LeaveApplicationForm, FeePaymentForm
)

@login_required
def dashboard(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Get student's enrollments
    enrollments = request.user.enrollments.all()
    
    # Summary data
    total_courses = enrollments.count()
    active_courses = enrollments.filter(status='active').count()
    completed_courses = enrollments.filter(status='completed').count()
    
    # Get certificates
    certificates = request.user.certificates.all()
    
    # Get recent results
    recent_results = ExamResult.objects.filter(
        enrollment__student=request.user
    ).order_by('-created_at')[:5]
    
    # Get upcoming assignments
    today = timezone.now().date()
    upcoming_assignments = Assignment.objects.filter(
        course__in=[e.course for e in enrollments.filter(status='active')],
        due_date__gte=today
    ).order_by('due_date')[:5]
    
    # Get attendance summary
    attendance_records = Attendance.objects.filter(
        user=request.user,
        attendee_type='student'
    )
    
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    # Get fee status
    pending_fees = FeePayment.objects.filter(
        student=request.user,
        is_verified=False
    ).count()
    
    # Get leave applications
    leave_applications = request.user.leave_applications.all().order_by('-applied_at')[:3]
    
    context = {
        'total_courses': total_courses,
        'active_courses': active_courses,
        'completed_courses': completed_courses,
        'certificates': certificates,
        'recent_results': recent_results,
        'upcoming_assignments': upcoming_assignments,
        'attendance_percentage': attendance_percentage,
        'pending_fees': pending_fees,
        'leave_applications': leave_applications,
    }
    
    return render(request, 'StudentApp/dashboard.html', context)

@login_required
def academics(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Get student's enrollments
    enrollments = request.user.enrollments.all()
    
    # Get attendance records
    attendance_records = Attendance.objects.filter(
        user=request.user,
        attendee_type='student'
    ).order_by('-date')
    
    # Get exam results
    exam_results = ExamResult.objects.filter(
        enrollment__student=request.user
    ).order_by('-created_at')
    
    # Calculate overall performance
    if exam_results.exists():
        overall_percentage = exam_results.aggregate(Avg('percentage'))['percentage__avg']
    else:
        overall_percentage = 0
    
    context = {
        'enrollments': enrollments,
        'attendance_records': attendance_records,
        'exam_results': exam_results,
        'overall_percentage': overall_percentage,
    }
    
    return render(request, 'StudentApp/academics.html', context)

@login_required
def finance(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Get fee payments
    fee_payments = request.user.fee_payments.all().order_by('-payment_date')
    
    # Calculate total fees paid
    total_paid = fee_payments.filter(is_verified=True).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get pending payments
    pending_payments = fee_payments.filter(is_verified=False)
    
    # Get enrollments with fee status
    enrollments = request.user.enrollments.all()
    
    context = {
        'fee_payments': fee_payments,
        'total_paid': total_paid,
        'pending_payments': pending_payments,
        'enrollments': enrollments,
    }
    
    return render(request, 'StudentApp/finance.html', context)

@login_required
def resources(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Get student's enrollments
    enrollments = request.user.enrollments.filter(status='active')
    
    # Get courses with syllabus
    courses_with_syllabus = [e.course for e in enrollments if e.course.syllabus]
    
    # Get lesson plans for enrolled courses
    lesson_plans = LessonPlan.objects.filter(
        course__in=[e.course for e in enrollments]
    ).order_by('-date')
    
    # Get assignments for enrolled courses
    assignments = Assignment.objects.filter(
        course__in=[e.course for e in enrollments]
    ).order_by('-due_date')
    
    context = {
        'courses_with_syllabus': courses_with_syllabus,
        'lesson_plans': lesson_plans,
        'assignments': assignments,
    }
    
    return render(request, 'StudentApp/resources.html', context)

@login_required
def certificates(request):
    # Get student's certificates
    certificates = Certificate.objects.filter(student=request.user)
    
    # Get completed enrollments without certificates
    completed_enrollments = Enrollment.objects.filter(
        student=request.user,
        status='completed'
    )
    
    # Get course IDs from certificates
    certificate_course_ids = certificates.values_list('course_id', flat=True)
    
    # Filter out completed enrollments that already have certificates
    completed_enrollments_without_certificates = completed_enrollments.exclude(
        course_id__in=certificate_course_ids
    )
    
    # Calculate counts
    certified_count = certificates.count()
    completed_count = completed_enrollments.count()
    pending_count = completed_enrollments_without_certificates.count()
    
    # Calculate online/offline certificate counts
    online_certificates = certificates.filter(course__course_type='online')
    offline_certificates = certificates.filter(course__course_type='offline')
    online_count = online_certificates.count()
    offline_count = offline_certificates.count()
    
    context = {
        'certificates': certificates,
        'completed_enrollments': completed_enrollments_without_certificates,
        'certified_count': certified_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'online_count': online_count,
        'offline_count': offline_count,
    }
    
    return render(request, 'StudentApp/certificates.html', context)

@login_required
def courses(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    # Get all available courses
    available_courses = Course.objects.filter(status='active')
    
    # Get student's enrollments
    enrollments = request.user.enrollments.all()
    enrolled_course_ids = [e.course.id for e in enrollments]
    
    # Filter out already enrolled courses
    courses_to_enroll = available_courses.exclude(id__in=enrolled_course_ids)
    
    context = {
        'available_courses': available_courses,
        'courses_to_enroll': courses_to_enroll,
        'enrollments': enrollments,
    }
    
    return render(request, 'StudentApp/courses.html', context)

@login_required
def enroll_course(request, course_id):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, "You are already enrolled in this course.")
        return redirect('student_courses')
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.course = course
            enrollment.save()
            messages.success(request, f"You have successfully enrolled in {course.title}!")
            return redirect('student_courses')
    else:
        form = EnrollmentForm()
    
    context = {
        'form': form,
        'course': course,
    }
    
    return render(request, 'StudentApp/enroll_course.html', context)

@login_required
def apply_leave(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.student = request.user
            leave_application.save()
            messages.success(request, "Your leave application has been submitted successfully!")
            return redirect('student_academics')
    else:
        form = LeaveApplicationForm()
    
    return render(request, 'StudentApp/apply_leave.html', {'form': form})

@login_required
def make_payment(request):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = request.user
            payment.save()
            messages.success(request, "Your payment has been submitted successfully! It will be verified soon.")
            return redirect('student_finance')
    else:
        form = FeePaymentForm()
    
    return render(request, 'StudentApp/make_payment.html', {'form': form})

@login_required
def apply_certificate(request, course_id):
    # Only students can access this
    if request.user.role != 'student':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard_redirect')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Check if enrollment exists and is completed
    enrollment = Enrollment.objects.filter(student=request.user, course=course, status='completed').first()
    if not enrollment:
        messages.error(request, "You need to complete the course before applying for a certificate.")
        return redirect('student_certificates')
    
    # Check if certificate already exists
    if Certificate.objects.filter(student=request.user, course=course).exists():
        messages.error(request, "You already have a certificate for this course.")
        return redirect('student_certificates')
    
    if request.method == 'POST':
        # Create certificate
        certificate = Certificate(
            student=request.user,
            course=course,
            certificate_type=course.course_type,
            certificate_number=f"CERT-{request.user.id}-{course.id}-{timezone.now().strftime('%Y%m%d')}"
        )
        certificate.save()
        messages.success(request, "Your certificate application has been submitted successfully!")
        return redirect('student_certificates')
    
    context = {
        'course': course,
        'enrollment': enrollment,
    }
    
    return render(request, 'StudentApp/apply_certificate.html', context)