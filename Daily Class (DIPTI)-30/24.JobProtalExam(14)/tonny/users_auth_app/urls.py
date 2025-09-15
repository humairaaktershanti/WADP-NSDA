from django.contrib import admin
from django.urls import path
from users_auth_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registerpage, name='registerpage'),
    path('loginpage/', loginpage, name='loginpage'),
   
    path('change_pass/', change_pass, name='change_pass'),
    path('logoutpage/', logoutpage, name='logoutpage'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('list_pending/', list_pending, name='list_pending'),
]