
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',book_form,name='book_form'),
    path('book_list/',book_list,name='book_list'),
    path('book_confirm_delete/',book_confirm_delete,name='book_confirm_delete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
