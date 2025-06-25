
from django.contrib import admin
from django.urls import path
from studentTodoSystemProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('addStudent/',addStudent,name="addStudent"),
    path('studentList/',studentList,name="studentList"),
    path('addTask/',addTask,name="addTask"),
    path('taskList/',taskList,name="taskList"),
    
    path('viewStudent/<int:id>',viewStudent,name='viewStudent'),
    path('deleteStudent/<int:id>',deleteStudent,name='deleteStudent'),
    path('viewTask/<int:id>',viewTask,name='viewTask'),
    path('deleteTask/<int:id>',deleteTask,name='deleteTask'),
    path('editStudent/<int:id>',editStudent,name='editStudent'),
    path('editTask/<int:id>',editTask,name='editTask'),

    path('SignUp/',SignUp,name='SignUp'),
    path('Login/',Login,name='Login'),
    path('logOut/',logOut,name='logOut'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
