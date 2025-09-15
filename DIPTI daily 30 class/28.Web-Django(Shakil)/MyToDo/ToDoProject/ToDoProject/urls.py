from django.contrib import admin
from django.urls import path
from ToDoProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signupPage,name="signupPage"),
    path('signinPage/',signinPage,name="signinPage"),
    path('logoutPage/',logoutPage,name="logoutPage"),
    path('dashboard/',dashboard,name="dashboard"),
    
    path('addCategory/',addCategory,name="addCategory"),
    path('categoryList/',categoryList,name="categoryList"),
]
