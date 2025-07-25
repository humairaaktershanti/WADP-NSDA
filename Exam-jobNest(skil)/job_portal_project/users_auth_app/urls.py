from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('register/', register, name='register'),
    path('login/', logIn, name='login'),
    path('logOut/', logOut, name='logOut'),
    path('change_password/', change_password, name='change_password'),
]