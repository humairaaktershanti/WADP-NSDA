
from django.contrib import admin
from django.urls import path
from libraryApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('addBook/',addBook,name='addBook'),
    path('listBook/',listBook,name='listBook'),
    path('viewBook/<int:id>',viewBook,name='viewBook'),
    path('editBook/<int:id>',editBook,name='editBook'),
    path('deleteBook/<int:id>',deleteBook,name='deleteBook'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
