from django.contrib import admin
from django.urls import path
from practice_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('author/',author,name='author'),
    path('book/',book,name='book'),
]
