from django.contrib import admin
from django.urls import path
from recipeProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('addRecipe/',addRecipe,name='addRecipe'),
    path('RecipeList/',RecipeList,name='RecipeList'),
    path('deleteRecipe/<int:id>',deleteRecipe,name='deleteRecipe'),
    path('viewsRecipe/<int:id>',viewsRecipe,name='viewsRecipe'),
    path('editRecipe/<int:id>',editRecipe,name='editRecipe'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
