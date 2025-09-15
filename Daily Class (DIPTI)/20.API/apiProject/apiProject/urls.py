

from django.contrib import admin
from django.urls import path

from apiApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/studentList/', studentList, name='studentList'),
    path('api/add_student/', add_student, name='add_student'),
]
