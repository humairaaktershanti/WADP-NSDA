from django.contrib import admin
from django.urls import path
from ResumeBuilder.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',resume,name='resume'),
    path('addresume/',addresume,name='addresume'),
    path('updateresume/',updateresume,name='updateresume'),
    path('editresume/<str:myid>',editresume,name='editresume'),
    path('viewresume/<str:myid>',viewresume,name='viewresume'),
    path('deleteresume/<str:myid>',deleteresume,name='deleteresume'),
]
