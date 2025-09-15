from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    userType=models.CharField(choices=[
        ('Admin','Admin'),
        ('Teacher','Teacher'),
    ],null=True)


