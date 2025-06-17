from django.db import models

# Create your models here.
class RecipeModel(models.Model):
    Title=models.TextField(max_length=100)
    Description=models.TextField(max_length=100)
    Ingredients=models.TextField(max_length=100)
    Instructions=models.TextField(max_length=100)
    Image=models.ImageField(upload_to="Media/Photo")    