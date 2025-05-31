
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
    

]
