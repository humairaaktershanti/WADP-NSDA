# urls.py
from django.urls import path
from employeeApp.views import *

urlpatterns = [
    path('employee-dashboard/', employee_dashboard, name='employee_dashboard'),

    path('leaves-employee/', leaves_employee, name='leaves_employee'),
    path("leaves/add/", add_leave, name="add_leave"),
    path("leaves/<int:pk>/edit/", edit_leave, name="edit_leave"),
    path("leaves/<int:pk>/delete/", delete_leave, name="delete_leave"),

    path('attendance_dashboard/', attendance_dashboard, name='attendance_dashboard'),
    path('attendances/', attendance_list, name='attendance_list'),
    path('attendances/add/', add_attendance, name='add_attendance'),
    path('attendances/<int:pk>/edit/', edit_attendance, name='edit_attendance'),
    path('attendances/<int:pk>/delete/', delete_attendance, name='delete_attendance'),
    path('leave-history/', leave_history, name='leave_history'),
    path('leave-history/<int:pk>/edit/', edit_leave, name='edit_leave'),
    path('leave-history/<int:pk>/delete/', delete_leave, name='delete_leave'),

    path('leave/<int:pk>/edit/', edit_leave, name="edit_leave"),
    path('leave/<int:pk>/delete/', delete_leave, name="delete_leave"),
    path('leave/<int:pk>/', leave_detail, name="leave_detail"),

    path('activities/', employee_activities, name='employee_activities'),

    path('tasks/', task_list, name='task_list'),
    path('tasks-board/', task_board, name='task_board'),
    path('tasks/add/', add_task, name='add_task'),
    path('tasks/<int:pk>/edit/', edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', delete_task, name='delete_task'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('tasks/<int:pk>/update-status/', update_task_status, name='update_task_status'),

    path('resignation/', resignation, name='resignation'),
    path('add_resignation/', add_resignation, name='add_resignation'),
    path('edit_resignation/<int:pk>/', edit_resignation, name='edit_resignation'),
    path('delete_resignation/<int:pk>/', delete_resignation, name='delete_resignation'),
    path('employee_profile/', employee_profile, name='employee_profile'),
    path('employee_certificate/<int:profile_id>/', employee_certificate, name='employee_certificate'),
]