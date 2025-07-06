
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name='home'),
    path('signUp/',signUp,name='signUp'),
    path('',logIn,name='logIn'),
    path('logOut/',logOut,name='logOut'),
    path('changePassword/',changePassword,name='changePassword'),
]
