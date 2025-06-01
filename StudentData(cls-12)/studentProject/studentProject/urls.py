
from django.contrib import admin
from django.urls import path
from studentProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('addStudent/', addStudent, name='addStudent'),
    path('studentList/', studentList, name='studentList'),
    path('addTeacher/', addTeacher, name='addTeacher'),
    path('TeacherList/', TeacherList, name='TeacherList'),
    path('addCourse/', addCourse, name='addCourse'),
    path('courseList/', courseList, name='courseList'),
    path('DeleteStudent/<str:myid>/', DeleteStudent, name='DeleteStudent'),
    path('DeleteTeacher/<str:myid>/', DeleteTeacher, name='DeleteTeacher'),
    path('DeleteCourse/<str:myid>/', DeleteCourse, name='DeleteCourse'),



]
