
from django.contrib import admin
from django.urls import path
from eventApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',home,name='home'),
    path('addEvent/',addEvent,name='addEvent'),
    path('listEvent/',listEvent,name='listEvent'),

    path('deleteEvent/<int:id>',deleteEvent,name='deleteEvent'),
    path('veiwEvent/<int:id>',veiwEvent,name='veiwEvent'),
    path('editEvent/<int:id>',editEvent,name='editEvent'),

    path('signUp/',signUp,name='signUp'),
    path('logIn/',logIn,name='logIn'),
    path('logOut/',logOut,name='logOut'),
    path('changepass/',changepass,name='changepass'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
