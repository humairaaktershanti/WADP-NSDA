from django.db import models

# Create your models here.
class recipeModel(models.Model):
    name=models.CharField(max_length=100,null=True)
    ingredients=models.TextField(null=True)
    instructions=models.TextField(null=True)
    image=models.ImageField(upload_to='media/photp',null=True)
    creator=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    created_at=models.DateField(auto_now_add=True,null=True)