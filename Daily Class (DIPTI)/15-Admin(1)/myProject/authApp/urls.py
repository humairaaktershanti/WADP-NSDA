from django.urls import path
from authApp.views import *


urlpatterns = [ 
    path('',home,name='home'),
    path('signUp/',signUp,name='signUp'),
    path('logIn/',logIn,name='logIn'),
    path('logOut/',logOut,name='logOut'),

    
    path('addTeacher/',addTeacher,name='addTeacher'),
    path('addStudent/',addStudent,name='addStudent'),
    path('pendingStudent/',pendingStudent,name='pendingStudent'),
    path('approved/<int:id>',approved,name='approved'),


    path('forgotPass/',forgotPass,name='forgotPass'),


]
