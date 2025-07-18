
from django.contrib import admin
from django.urls import path
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('formTask/',formTask,name='formTask'),
    path('listTask/',listTask,name='listTask'),
    path('deleteTask/<int:id>',deleteTask,name='deleteTask'),
    path('editTask/<int:id>',editTask,name='editTask'),
    path('viewsTask/<int:id>',viewsTask,name='viewsTask'),

]
