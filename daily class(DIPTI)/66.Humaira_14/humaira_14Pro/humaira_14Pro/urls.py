
from django.contrib import admin
from django.urls import path
from authApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signUp/', signUp,name='signUp'),
    path('', logIn,name='logIn'),
    path('logOut/', logOut,name='logOut'),
    path('index/', index,name='index'),

]
