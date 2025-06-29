
from django.contrib import admin
from django.urls import path
from myApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('recipeCreate/',recipeCreate,name='recipeCreate'),
    path('recipeList/',recipeList,name='recipeList'),
    path('deleteRecipe/<int:id>', deleteRecipe,name='deleteRecipe'),
    path('ViewRecipe/<int:id>', ViewRecipe,name='ViewRecipe'),
    path('editRecipe/<int:id>', editRecipe,name='editRecipe'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
