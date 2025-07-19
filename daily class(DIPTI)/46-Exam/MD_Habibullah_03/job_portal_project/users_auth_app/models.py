from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUserModel(AbstractUser):
    USER_TYPES = (
        ('Admin', 'Admin'),
        ('Employer', 'Employer'),
        ('Candidate', 'Candidate'),
    )
    phone = models.CharField(max_length=20)
    user_types = models.CharField(max_length=10, choices=USER_TYPES)


class PendingAccountModel(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accept', 'Accept'),
        ('Rejected', 'Rejected'),
    )

    USER_TYPE_CHOICES = (
        ('Employer', 'Employer'),
        ('Candidate', 'Candidate'),
    )
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    user_types = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    pending_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')



