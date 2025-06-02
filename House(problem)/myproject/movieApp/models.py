from django.db import models

# Create your models here.
class movie(models.Model):
    name = models.CharField(max_length=50)
    year = models.DateField()
    genre=models.CharField(max_length=100) 
    rating=models.ImageField()
    duration=models.IntegerField()
    director=models.CharField(max_length=50)