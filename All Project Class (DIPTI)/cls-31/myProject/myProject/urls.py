
from django.contrib import admin
from django.urls import path
from myApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name='home'),
    path('formTask/',formTask,name='formTask'),
    path('listTask/',listTask,name='listTask'),
    path('deleteTask/<int:id>',deleteTask,name='deleteTask'),
    path('editTask/<int:id>',editTask,name='editTask'),
    path('viewsTask/<int:id>',viewsTask,name='viewsTask'),
    path('signUp/',signUp,name='signUp'),
    path('',signIn,name='signIn'),
    path('logout/',logout,name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
