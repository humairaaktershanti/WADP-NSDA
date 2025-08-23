from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('setup/', views.setup_view, name='setup'),
    path('create-admin/', views.create_admin_view, name='create_admin'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]