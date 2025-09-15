from django.contrib import admin
from django.urls import path
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('login/',logIn,name='login'),
    path('logOut/',logOut,name='logOut'),
    path('change_password/',change_password,name='change_password'),
    path('dashboard_recruiter/',dashboard_recruiter,name='dashboard_recruiter'),
    path('dashboard_seeker/',dashboard_seeker,name='dashboard_seeker'),
    path('profile_recruiter/',profile_recruiter,name='profile_recruiter'),
    path('job_post/',job_post,name='job_post'),
    path('dashboard_seeker/',dashboard_seeker,name='dashboard_seeker'),
    path('job_list/',job_list,name='job_list'),
    path('profile_seeker/',profile_seeker,name='profile_seeker'),
]