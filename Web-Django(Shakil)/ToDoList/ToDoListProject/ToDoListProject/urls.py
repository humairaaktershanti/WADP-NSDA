from django.contrib import admin
from django.urls import path
from ToDoListProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signupPage,name='signupPage'),
    path('signinPage/',signinPage,name='signinPage'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logoutPage/',logoutPage,name='logoutPage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
