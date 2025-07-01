from django.contrib import admin
from django.urls import path
from toDoApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', name='index'),
    path('', logIn, name='logIn'),
    path('signUp/', signUp, name='signUp'),
    path('logOut/', logOut, name='logOut'),
    path('updatePassword/', updatePassword, name='updatePassword'),
]