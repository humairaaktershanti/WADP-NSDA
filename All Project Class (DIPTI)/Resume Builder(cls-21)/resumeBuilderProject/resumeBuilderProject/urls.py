
from django.contrib import admin
from django.urls import path
from resumeBuilderProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',formResume,name='formResume'),
    path('listResume/',listResume,name='listResume'),
    path('deleteResume/<int:id>',deleteResume,name='deleteResume'),
    path('viewResume/<int:id>',viewResume, name='viewResume')
    path('editResume/<int:id>',editResume, name='editResume')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
