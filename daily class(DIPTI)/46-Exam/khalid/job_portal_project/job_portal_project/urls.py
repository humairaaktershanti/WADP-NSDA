from django.contrib import admin
from django.urls import path
from users_auth_app.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    path('signUp/', signUp,name='signUp'),
    path('logIn/', logIn,name='logIn'),
    path('logOut/', logOut,name='logout'),
    path('changePassword/', changePassword,name='changePassword'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)