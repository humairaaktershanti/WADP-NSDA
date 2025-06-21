
from django.contrib import admin
from django.urls import path
from myAPP.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',create,name='create'),
    path('read/',read,name='read'),
    path('edit/<int:id>',edit,name='edit'),
    path('delete/<int:id>',delete,name='delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
