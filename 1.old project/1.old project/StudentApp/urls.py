from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='student_dashboard'),
    path('academics/', views.academics, name='student_academics'),
    path('finance/', views.finance, name='student_finance'),
    path('resources/', views.resources, name='student_resources'),
    path('certificates/', views.certificates, name='student_certificates'),
    path('courses/', views.courses, name='student_courses'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('apply-certificate/<int:course_id>/', views.apply_certificate, name='apply_certificate'),
]