from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='employee_dashboard'),
    
    # Faculty URLs
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    
    # HR URLs
    path('hr/', views.hr_dashboard, name='hr_dashboard'),
    path('hr/job-posts/', views.job_post_list, name='job_post_list'),
    path('hr/job-posts/create/', views.job_post_create, name='job_post_create'),
    
    # Finance URLs
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('finance/salaries/', views.salary_list, name='salary_list'),
    path('finance/salaries/create/', views.salary_create, name='salary_create'),
    path('finance/expenses/', views.expense_list, name='expense_list'),
    path('finance/expenses/create/', views.expense_create, name='expense_create'),
    
    # Teacher URLs
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Other URLs
    path('other/', views.other_dashboard, name='other_dashboard'),
    
    # Common URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
]