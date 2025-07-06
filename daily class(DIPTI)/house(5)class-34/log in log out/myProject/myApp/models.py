from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    fullName=models.CharField(max_length=100,null=True)
    bio=models.TextField(null=True)
    userType=models.CharField(max_length=100,choices=[
        ('Teacher','Teacher'),
        ('Student','Student'),
    ],null=True)
    