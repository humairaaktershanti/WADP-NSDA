from django.urls import path
from user_auth_app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('setup/', setupPage, name='setupPage'),
    path('loginPage/', loginPage, name='loginPage'),
    path('logout/', logoutPage, name='logoutPage'),
    path('register/', registerPage, name='registerPage'),
   
    # Profile
    path('profileInfo/', profileInfo, name='profileInfo'),
    path('editProfile/', editProfile, name='editProfile'),
    path('changePasswordPage/', changePasswordPage, name='changePasswordPage'),





    # ------Role-Based Dashboards
    # path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    # path('faculty/dashboard/', faculty_dashboard, name='faculty_dashboard'),
    # path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    # path('student/dashboard/', student_dashboard, name='student_dashboard'),
    # path('candidate/dashboard/', candidate_dashboard, name='candidate_dashboard'),
    # path('employee/dashboard/', employee_dashboard, name='employee_dashboard'),

   

    # ------Admin: Create User
    # path('admin/create-user/', create_user_view, name='create_user_view'),
]


