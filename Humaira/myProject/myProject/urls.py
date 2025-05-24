from django.contrib import admin
from django.urls import path
from myProject.views import homePage, logIn


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homePage, name='homepage'),
    path('login/',logIn, name='login'),
]