from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    bio=models.TextField(null=True)
    image=models.ImageField(upload_to='media/photo',null=True)
    address=models.TextField(null=True)
    userType=models.CharField(max_length=100,choices=[
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ],null=True)


