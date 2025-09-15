from django.contrib import admin
from django.urls import path
from storeProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',storePage,name="storePage"),
    path('addStore/',addStore,name="addStore"),
    path('updateStore/',updateStore,name="updateStore"),
    path('deleteStore/<str:myid>',deleteStore,name="deleteStore"),
    path('editStore/<str:myid>',editStore,name="editStore"),
    path('viewStore/<str:myid>',viewStore,name="viewStore")
    
]
