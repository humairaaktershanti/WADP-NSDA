from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('logIn/', logIn, name='logIn'),
    path('SignUp/', SignUp, name='SignUp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('change_password/', change_password, name='change_password'),
    path('update_profile/', update_profile, name='update_profile'),
    path('logOut/', logOut, name='logOut'),
]