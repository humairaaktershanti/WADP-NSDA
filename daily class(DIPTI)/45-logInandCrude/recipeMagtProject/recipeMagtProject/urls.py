
from django.contrib import admin
from django.urls import path
from recipeApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name="home"),
    path('signUp/',signUp,name="signUp"),
    path('',logIn,name="logIn"),
    path('logOut/',logOUT,name="logOut"),
    path('Addrecipe/',Addrecipe,name="Addrecipe"),
    path('listRecipe/',listRecipe,name="listRecipe"),

    path('editRecipe/<int:id>',editRecipe,name="editRecipe"),
    path('deleteRecipe/<int:id>',deleteRecipe,name="deleteRecipe"),
    path('viewRecipe/<int:id>',viewRecipe,name="viewRecipe"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
