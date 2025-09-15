
from django.contrib import admin
from django.urls import path
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('login/',logIn,name='login'),
    path('logOut/',logOut,name='logOut'),
    path('change_password/',change_password,name='change_password'),
    # path('job_post/',job_post,name='job_post'),
]
