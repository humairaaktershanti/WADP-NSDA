from django.db import models

# Create your models here.
class recipeModel(models.Model):
    Title=models.CharField(max_length=100)
    Description=models.CharField(max_length=100)
    Ingredients=models.CharField(max_length=100)
    Instructions=models.CharField(max_length=100)
    Image=models.ImageField(upload_to="Media/Photo")