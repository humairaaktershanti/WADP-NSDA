from django.db import models

# Create your models here.
class studetnModel(models.Model):
    FirstName=models.CharField(max_length=50,null=True)
    LastName=models.CharField(max_length=50,null=True)
    Department=models.CharField(max_length=50,null=True)
    City=models.CharField(max_length=50,null=True)
    
class teacherModel(models.Model):
    FirstName=models.CharField(max_length=50,null=True)
    LastName=models.CharField(max_length=50,null=True)
    Department=models.CharField(max_length=50,null=True)
    City=models.CharField(max_length=50,null=True)
