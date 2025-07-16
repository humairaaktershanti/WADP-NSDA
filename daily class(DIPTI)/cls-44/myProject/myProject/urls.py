
from django.contrib import admin
from django.urls import path
from authApp.views import *
from courseApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('signUp/',signUp,name='signUp'),
    path('logIn/',logIn,name='logIn'),
]
