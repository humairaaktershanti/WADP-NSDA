
from django.contrib import admin
from django.urls import path
from movieModel.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('addMovie/',addMovie,name='addMovie'),
    path('listMovie/',listMovie,name='listMovie'),
    path('viewMovie/<int:id>',viewMovie,name='viewMovie'),
    path('editMovie/<int:id>',editMovie,name='editMovie'),
    path('deleteMovie/<int:id>',deleteMovie,name='deleteMovie'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
