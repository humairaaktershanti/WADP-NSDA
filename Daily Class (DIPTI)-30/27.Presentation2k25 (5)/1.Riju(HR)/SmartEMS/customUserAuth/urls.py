from django.urls import path
from customUserAuth.views import *

urlpatterns = [
    path('', homePage, name='home'),
    path('log-in/', logIn, name='logIn'),
    path('register/', signUp, name='signUp'),
    path('change-password/', change_password, name='changePassword'),
    path('log-out/', logOut, name='logOut'),
    path('lock-screen/', lock_screen, name='lock_screen'),

]