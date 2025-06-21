
from django.contrib import admin
from django.urls import path
from myApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',formManager,name='formManager'),
    path('listManager/',listManager,name='listManager'),
    path('updateManager/<int:id>',updateManager,name='updateManager')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
