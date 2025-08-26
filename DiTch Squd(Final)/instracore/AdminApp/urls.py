from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Dashboard API endpoints
    path('api/dashboard/attendance/', views.dashboard_attendance, name='dashboard_attendance'),
    path('api/dashboard/courses/', views.dashboard_courses, name='dashboard_courses'),
    path('api/dashboard/weekend-days/', views.dashboard_weekend_days, name='dashboard_weekend_days'),
    
    # Create endpoints
    path('create/user/', views.create_user, name='create_user'),
    path('create/notice/', views.create_notice, name='create_notice'),
    path('create/event/', views.create_event, name='create_event'),
    path('create/financial/', views.create_financial_data, name='create_financial_data'),
    
    # Export endpoints
    path('export/student/', views.export_data, {'data_type': 'student'}, name='export_student_data'),
    path('export/employee/', views.export_data, {'data_type': 'employee'}, name='export_employee_data'),
    path('export/course/', views.export_data, {'data_type': 'course'}, name='export_course_data'),
    path('export/account/', views.export_data, {'data_type': 'account'}, name='export_account_data'),

    path('user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]