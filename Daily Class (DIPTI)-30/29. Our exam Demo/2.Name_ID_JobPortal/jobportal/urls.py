from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job_view, name='apply_job'),
    path('upload-resume/', views.upload_resume_view, name='upload_resume'),
    path('applications/', views.applications_view, name='applications'),
    path('application/<int:application_id>/update-status/', views.update_application_status_view, name='update_application_status'),
]