
from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='Home'),
    path('Resturent/', Resturent, name='Resturent'),
    path('AddResturent/', AddResturent, name='AddResturent'),
]
