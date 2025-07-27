

from django.contrib import admin
from django.urls import path

from apiApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/studentList/', studentList, name='studentList'),
]
