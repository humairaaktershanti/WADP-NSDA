from django.urls import path
from courseApp.views import *


urlpatterns = [ 
    path('addAdmitted/',addAdmitted,name='addAdmitted'),
    path('addCourse/',addCourse,name='addCourse'),
    
    


]
