from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('users/', views.users, name='admin_users'),
    path('users/create-employee/', views.create_employee, name='create_employee'),
    path('users/create-admin/', views.create_admin, name='create_admin'),
    path('courses/', views.courses, name='admin_courses'),
    path('attendance/', views.attendance, name='admin_attendance'),
    path('events/', views.events, name='admin_events'),
    path('accounts/', views.accounts, name='admin_accounts'),
    path('reports/', views.reports, name='admin_reports'),
]