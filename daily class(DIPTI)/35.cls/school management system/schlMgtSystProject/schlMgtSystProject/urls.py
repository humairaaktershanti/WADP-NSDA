
from django.contrib import admin
from django.urls import path
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('logIn/',logIn,name='logIn'),
    path('signUp/',signUp,name='signUp'),
    path('logOut/',logOut,name='logOut'),
    path('changePassword/',changePassword,name='changePassword'),
    
]
