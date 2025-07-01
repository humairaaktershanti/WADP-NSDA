from django.contrib import admin
from django.urls import path
from toDoApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index, name='index'),

    path('', logIn, name='logIn'),
    path('signUp/', signUp, name='signUp'),
    path('logOut/', logOut, name='logOut'),
    path('updatePassword', updatePassword, name='updatePassword'),

    path('addToDo/', addToDo, name='addToDo'),
    path('listToDo/', listToDo, name='listToDo'),

    path('deleteToDo/<str:id>', deleteToDo, name='deleteToDo'),
    path('viewsToDo/<str:id>', viewsToDo, name='viewsToDo'),
    path('editToDo/<str:id>', editToDo, name='editToDo'),

    path('DoneToDo/', DoneToDo, name='DoneToDo'),
]