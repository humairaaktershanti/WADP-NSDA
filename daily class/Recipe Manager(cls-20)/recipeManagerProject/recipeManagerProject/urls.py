
from django.contrib import admin
from django.urls import path
from recipeManagerProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeList,name='homeList'),
    path('addRecipe',addRecipe,name='addRecipe'),
    path('viewTask/<int:id>',viewTask,name='viewTask'),
    path('delete/<int:id>',delete,name='delete'),
    path('edit/<int:id>',edit,name='edit'),


    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
