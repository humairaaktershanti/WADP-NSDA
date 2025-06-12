from todo_project.views import *
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('addTask',addTask,name='addTask'),
    path('taskList',taskList, name='taskList'),
]