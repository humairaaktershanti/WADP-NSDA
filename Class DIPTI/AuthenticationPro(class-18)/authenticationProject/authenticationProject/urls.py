
from django.contrib import admin
from django.urls import path
from authenticationProject.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name='home'),
    path('registration/',registration,name='home'),
    path('',login,name='login')
]

