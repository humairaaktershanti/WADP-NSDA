from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logoutPage/', views.logoutPage, name='logout'),
    path('change_password/', views.change_password, name='change_password'),


    path('dashboard/', views.DashboardPage, name='dashboard'),
 
]