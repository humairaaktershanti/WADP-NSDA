from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recipeProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signinPage,name="signinPage"),
    path('signupPage/',signupPage,name="signupPage"),
    path('dashboard/',dashboard,name="dashboard"),
    path('profileView/',profileView,name="profileView"),
    path('logoupPage/',logoupPage,name="logoupPage"),
    
    path('addrecipePage/',addrecipePage,name="addrecipePage"),
    path('recipelistPage/',recipelistPage,name="recipelistPage"),
    path('updaterecipePage/',updaterecipePage,name="updaterecipePage"),
    path('editrecipe/<str:recipeid>',editrecipe,name="editrecipe"),
    path('deleterecipe/<str:recipeid>',deleterecipe,name="deleterecipe"),
    path('viewrecipe/<str:recipeid>',viewrecipe,name="viewrecipe"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
