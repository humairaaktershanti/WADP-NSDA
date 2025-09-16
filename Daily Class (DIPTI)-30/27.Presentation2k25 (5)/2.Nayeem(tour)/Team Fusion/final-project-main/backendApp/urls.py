from django.urls import path
from .views import *

urlpatterns = [

    path('dashboard',dashboard_page, name='admin_dashboard'),
    path('dashboard/login/', loginpage, name='dashboard_login'),
    path('dashboard/logout/', logout_view, name='dashboard_logout'),
    path('dashboard/guides/', guide_management, name='guide_management'),

]
