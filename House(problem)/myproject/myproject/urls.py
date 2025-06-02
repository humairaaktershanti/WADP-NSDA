
from django.contrib import admin
from django.urls import path
from myproject.views import movie
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie, name='movie'),
]
