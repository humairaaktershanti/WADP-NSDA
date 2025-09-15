from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Llibrary_User(AbstractUser):
    USER =[
        ('Seller','Seller'),
        ('Customer','Customer'),
    ]
    FullName = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    UserType = models.CharField(choices=USER,max_length=50)
    

    
    
    