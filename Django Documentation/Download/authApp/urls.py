from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('logIn/', logIn, name='logIn'),
    path('SignUp/', SignUp, name='SignUp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('change_password/', change_password, name='change_password'),
    path('update_profile/', update_profile, name='update_profile'),
    path('logOut/', logOut, name='logOut'),

    path('one/', one, name='one'),
    path('two/', two, name='two'),
    
    path('addToDo/', addToDo, name='addToDo'),
    path('listToDo/', listToDo, name='listToDo'),
    path('viewsToDo/<int:id>', viewsToDo, name='viewsToDo'),
    path('updateToDo/<int:id>', updateToDo, name='updateToDo'),
    path('deleteToDo/<int:id>', deleteToDo, name='deleteToDo'),
]