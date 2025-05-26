
from django.contrib import admin
from django.urls import path
from myProject.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homePage),
    path('signupPage/',signupPage, name="signupPage"),
    path('loginPage/',loginPage, name="loginPage"),

]
