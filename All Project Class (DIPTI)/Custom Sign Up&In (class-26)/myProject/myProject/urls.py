
from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signUp/',signUp,name='signUp'),
    path('signIn/',signIn,name='signIn'),
    path('',home,name='home'),
    path('logOut/',logOut,name='logOut')

]
