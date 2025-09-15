from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    USERTYPE = [
        ('Client','Client'),
        ('Guest','Guest'),
     
    ]
    userTypes = models.CharField(choices = USERTYPE, max_length = 100, null = True)
    fullName = models.CharField(max_length=100, null=True)
    phone= models.IntegerField(null=True)
