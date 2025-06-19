from django.db import models

# Create your models here.
class recipeModel(models.Model):

    RecipeTitle=models.TextField(max_length=50,null=True)
    RecipeImage=models.ImageField(upload_to='media/photo',null=True)
    Ingredients=models.TextField(max_length=100,null=True)
    Instruction=models.TextField(max_length=100,null=True)
    Category=models.CharField(max_length=100,null=True)
    Description=models.TextField(max_length=100,null=True)