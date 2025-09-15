from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUserModel(AbstractUser):
    phone=models.CharField(max_length=100,null=True)
    
    USER_TYPE=[
        ('admin','admin'),
        ('employer','employer'),
        ('candidate','candidate')
    ]

    user_type=models.CharField(max_length=100,choices=USER_TYPE)




class PendingAcountModel(models.Model):
    username=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=100,null=True)

    USER_TYPE=[
        ('employer','employer'),
        ('candidate','candidate'),
    ]
    user_type=models.CharField(max_length=100,choices=USER_TYPE)


    STATUS=[
        ('pending','pending'),
        ('accept','accept'),
        ('rejected','rejected')
    ]

    pending_status=models.CharField(max_length=100,choices=STATUS)




