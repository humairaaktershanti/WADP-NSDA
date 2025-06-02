from django.contrib import admin
from django.urls import path 
from DataSubProject.views import studentList, addStudent, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', studentList,name='studentList'),
    path('addStudent/', addStudent, name='addStudent'),
    path('contact/', contact, name='contact'),

]
