from django.db import models

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    age= models.IntegerField(null=True)

class teacher(models.Model):
    name = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    age= models.IntegerField(null=True)