from django.contrib import admin
from django.urls import path
from projectApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logIn/", logIn, name="logIn"),
    path("", index, name="index"),
    path("logOut/", logOut, name="logOut"),
    path("signUp/", signUp, name="signUp"),
    path('projectList/', projectList, name='projectList'),
    path('edit/<int:id>/', edit , name='edit'),
    path('view/<int:id>/', view , name='view'),
    path('delete/<int:id>/', delete , name='delete'),
    path('addProject/', addProject , name='addProject')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)