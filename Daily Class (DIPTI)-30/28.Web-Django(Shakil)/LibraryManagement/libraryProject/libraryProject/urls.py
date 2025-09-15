from django.contrib import admin
from django.urls import path
from libraryProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signinPage,name='signinPage'),
    path('signupPage/',signupPage,name='signupPage'),
    path('dashboard/',dashboard,name='dashboard'),
]
