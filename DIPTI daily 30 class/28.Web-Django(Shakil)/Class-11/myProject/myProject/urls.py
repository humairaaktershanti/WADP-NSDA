from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',studentpage,name="studentpage"),
    path('addstudent/',addstudent,name="addstudent"),
    path('deletestudent/<str:myid>',deletestudent,name="deletestudent"),
    path('editstudent/<str:myid>',editstudent,name="editstudent"),
    path('updatestudent/',updatestudent,name="updatestudent"),
    path('viewstudent/<str:myid>',viewstudent,name="viewstudent"),
    
]
