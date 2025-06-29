from django.db import models

# Create your models here.
class recipeModel(models.Model):
    title=models.CharField(max_length=100,null=True)
    description=models.TextField()
    ingredients=models.CharField(max_length=100,null=True)
    instructions=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='media/photo',null=True)