from django.urls import path, include
from .views import *


urlpatterns = [
    path('', logIn, name='logIn'),
    path('SignUp/', signUp, name='SignUp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logOut/', logOut, name='logOut'),
    path('profile/', profile, name='profile'),
]
