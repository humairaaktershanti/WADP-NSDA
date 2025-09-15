from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.StudentDashboardView.as_view(), name='dashboard'),
    # path('enroll-course/<int:course_id>/', views.EnrollCourseView.as_view(), name='enroll_course'),
    path('apply-certificate/', views.ApplyCertificateView.as_view(), name='apply_certificate'),

    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('enrollment/<int:enrollment_id>/', views.enrollment_details, name='enrollment_details'),
    path('payment/<int:enrollment_id>/', views.make_payment, name='make_payment'),
]