
from django.contrib import admin
from django.urls import path
from inventoryApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('addSupplier/',addSupplier,name='addSupplier'),
    path('listSupplier/',listSupplier,name='listSupplier'),

    path('viewSupplier/<int:id>',viewSupplier,name='viewSupplier'),
    path('deleteSupplier/<int:id>',deleteSupplier,name='deleteSupplier'),
    path('editSupplier/<int:id>',editSupplier,name='editSupplier'),
]