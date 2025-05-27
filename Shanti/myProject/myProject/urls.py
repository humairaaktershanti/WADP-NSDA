
from django.contrib import admin
from django.urls import path
from myProject.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',homePage),
    path('signupPage/',signupPage, name="signupPage"),
    path('loginPage/',loginPage, name="loginPage"),
    path('contactPage/',contactPage,name="contactPage"),
    path('newsPage/',newsPage,name="newsPage"),
    path('aboutPage/',aboutPage,name="aboutPage"),
    path('homePage/',homePage,name="homePage"),
]
