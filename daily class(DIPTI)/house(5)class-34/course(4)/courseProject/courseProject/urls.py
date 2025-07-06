
from django.contrib import admin
from django.urls import path
from courseApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('addCourse/',addCourse,name='addCourse'),
    path('listCourse/',listCourse,name='listCourse'),

    path('viewCourse/<int:id>',viewCourse,name='viewCourse'),
    path('deleteCourse/<int:id>',deleteCourse,name='deleteCourse'),
    path('editCourse/<int:id>',editCourse,name='editCourse'),
]