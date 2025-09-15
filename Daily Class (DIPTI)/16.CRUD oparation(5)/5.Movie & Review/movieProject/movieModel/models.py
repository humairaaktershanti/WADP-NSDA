from django.db import models

# Create your models here.
class movieModel(models.Model):
    title=models.CharField(max_length=100,null=True)
    releaseDate=models.DateField(auto_now=True,null=True)
    posterImage=models.ImageField(upload_to='media/photo',null=True)
    genre=models.CharField(max_length=100,null=True)
