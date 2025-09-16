from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    path('set-calorie-goal/', views.set_calorie_goal_view, name='set_calorie_goal'),
    path('calorie-history/', views.calorie_history_view, name='calorie_history'),
    path('delete-item/<int:item_id>/', views.delete_consumed_item_view, name='delete_item'),
]