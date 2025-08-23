from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    USERTYPE = [
        ('Admin','Admin'),
        ('Employee','Employee'),
        ('User','User')
    ]
    userTypes = models.CharField(choices = USERTYPE, max_length = 100, null = True)