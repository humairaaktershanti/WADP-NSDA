
from django.contrib import admin
from django.urls import path
from todo_DoProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='Home'),
    path('AddTask/', AddTask, name='AddTask'),
    path('TaskList/', TaskList, name='TaskList'),
    path('UpdateTask/<int:id>/', UpdateTask, name='UpdateTask'),
    path('DeleteTask/<int:id>/', DeleteTask, name='DeleteTask'),
]
