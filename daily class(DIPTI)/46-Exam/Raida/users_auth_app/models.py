from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserModel(AbstractUser):
    USER_TYPE = [
        ('Admin', 'Admin'),
        ('Employer', 'Employer'),
        ('Candidate', 'Candidate'),
    ]
    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='Candidate', null=True)

    def __str__(self):
        return self.username

class PendingAccountModel(models.Model):

    USER_TYPES = [
        ('Employer', 'Employer'),
        ('Candidate', 'Candidate'),
    ]

    PENDING_STATUS = [
        ('Pending', 'Pending'),
        ('Accept', 'Accept'),
        ('Rejected', 'Rejected'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)      
    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Candidate', null=True)
    pending_status = models.CharField(max_length=10, choices=PENDING_STATUS, default='Pending', null=True)
