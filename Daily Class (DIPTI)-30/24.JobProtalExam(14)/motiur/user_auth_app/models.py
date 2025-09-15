from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUserModel(AbstractUser):
    USER_TYPES=[
        ('Admin','Admin'),
        ('Employer','Employer'),
        ('Candidate','Candidate'),
    ]
    user_types = models.CharField(choices=USER_TYPES, max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)

class PendingAccountModel(models.Model):
    username = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    USER_TYPES=[
        ('Employer','Employer'),
        ('Candidate','Candidate'),
    ]
    user_types = models.CharField(choices=USER_TYPES, max_length=20, null=True)
    pending_status=[
        ('Pending','Pending'),
        ('Accept','Accept'),
        ('Rejected','Rejected'),
    ]
    pending_status = models.CharField(choices=pending_status, max_length=20, null=True)