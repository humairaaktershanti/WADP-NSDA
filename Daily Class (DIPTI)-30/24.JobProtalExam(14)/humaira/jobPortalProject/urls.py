
from django.contrib import admin
from django.urls import path
from userAuthApp.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('signUp/',signUp,name='signUp'),
    path('logIn/',logIn,name='logIn'),
    path('logOut/',logOut,name='logOut'),
    path('changePassword/',changePassword,name='changePassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
