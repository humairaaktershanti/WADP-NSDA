from django.contrib import admin
from django.urls import path
from bookingApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.hashers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Register/', Register, name='Register'),
    path('logIn/', logIn, name='logIn'),
    path('logOut/', logOut, name='logOut'),
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('addBooking/', addBooking, name='addBooking'),
    path('myBooking/', myBooking, name='myBooking'),
    path('update/<int:id>', update, name='update'),
    path('delete/<int:id>', delete, name='delete'),
    path('changePassword', changePassword, name='changePassword'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
