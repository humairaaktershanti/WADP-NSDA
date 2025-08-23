
from django.contrib import admin
from django.urls import path
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studentView/', studentView, name='studentView'),
]
