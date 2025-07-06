
from django.contrib import admin
from django.urls import path
from recipeManagerProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('formRecipes/',formRecipes,name='formRecipes'),
    path('ListRecipes/',ListRecipes,name='ListRecipes'),
    path('viewsRecipe/<int:id>',viewsRecipe,name='viewsRecipe'),
    path('editRecipe/<int:id>',editRecipe,name='editRecipe'),
    path('deleteRecipe/<int:id>',deleteRecipe,name='deleteRecipe'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
