from django.urls import path
from user_auth.views import *

urlpatterns = [
    path('',register,name='register'),
    path('loginpage/',loginpage,name='loginpage'),
    path('dashboard/',dashboard,name='dashboard'),
]
