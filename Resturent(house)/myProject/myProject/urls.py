
from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='Home'),
    path('AddResturent/', AddResturent, name='AddResturent'),
    # path('AddFood/', AddFood, name='AddFood'),
]
