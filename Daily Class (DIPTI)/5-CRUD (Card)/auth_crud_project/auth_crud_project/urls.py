
from django.contrib import admin
from django.urls import path
from auth_crud_project.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('addProduct/',addProduct,name='addProduct'),
    path('listProduct/',listProduct,name='listProduct'),
    path('viewProduct/<int:id>',viewProduct,name='viewProduct'),
    path('editProduct/<int:id>',editProduct,name='editProduct'),
    path('deleteProduct/<int:id>',deleteProduct,name='deleteProduct'),
    path('signUp/',signUp,name='signUp'),
    path('signIn/',signIn,name='signIn'),
    path('logOut/',logOut,name='logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
