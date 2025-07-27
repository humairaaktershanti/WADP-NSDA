from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    USER_TYPES=[
        ('Admin','Admin'),
        ('Employer', 'Employer'),
        ('Candidate', 'Candidate')
    ]
    phone=models.CharField(max_length=15)
    user_types=models.CharField(max_length=30, choices=USER_TYPES) 
    


class PendingAccountModel(models.Model):
    USERS=[
        ('Employer', 'Employer'),
        ('Candidate', 'Candidate'),
    ]

    STATUS=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    username=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    user_types=models.CharField(max_length=30, choices=USERS)
    pending_status=models.CharField(max_length=30, choices=STATUS, default='Pending')