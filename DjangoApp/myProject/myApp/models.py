from django.db import models

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dept = models.CharField(max_length=20)
    email= models.EmailField()
    bDay = models.DateField()

class teacher(models.Model):
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=20)
    email= models.EmailField()
    bDay = models.DateField()