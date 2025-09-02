from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logIn/', views.login_view, name='login'),
    path('SignUp/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', views.change_password, name='change_password'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logOut/', views.logout_view, name='logout'),
]