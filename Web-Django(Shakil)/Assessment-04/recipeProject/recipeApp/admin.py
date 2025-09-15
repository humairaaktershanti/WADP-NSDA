from django.contrib import admin
from recipeApp.models import *

# Register your models here.
class Recipe_User_Display(admin.ModelAdmin):
    list_display=['username','UserType','City']

class Recipe_Display(admin.ModelAdmin):
    list_display=['RecipeTitle','Create_by','RecipeCategory','DifficultyLevel']

    
admin.site.register(Recipe_User,Recipe_User_Display)
admin.site.register(addRecipeModel,Recipe_Display)

