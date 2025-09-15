from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home, name='homePage'),
    path('about/',about, name='aboutPage'),
    path('news/',news, name='newsPage'),
    path('contact/',contact, name='contactPage'),
]
