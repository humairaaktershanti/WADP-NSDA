from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',studentPage,name='studentPage'),
    path('addstudent/',addStudent,name='addStudent'),
    path('teacherPage/',teacherPage, name="teacherPage"),
    path('addteacher/',addTeacher,name="addteacher"),
]
