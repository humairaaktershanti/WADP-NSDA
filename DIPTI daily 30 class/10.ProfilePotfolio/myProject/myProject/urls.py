
from django.contrib import admin
from django.urls import path
from myProject.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signUp/',signUp,name='signUp'),
    path('signIn/',signIn,name='signIn'),
    path('',home,name='home'),
    path('logOut/',logOut,name='logOut')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
