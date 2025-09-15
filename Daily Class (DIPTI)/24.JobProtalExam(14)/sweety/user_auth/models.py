from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class customUserModel(AbstractUser):
    phone=models.CharField(max_length=100,null= True)
    user_type=models.CharField(max_length=100,null=True,choices=[
        ('Admin','Admin'),
        ('Employer','Employer'),
        ('Candidate','Candidate'),
        
    ])
    def __str__(self):
        return self.username

class PendingAccountModel(models.Model):
    username = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone =models.CharField(max_length=100,null=True)
    user_type = models.CharField(max_length=100,null=True,choices=[
        ('Employer','Employer'),
        ('Candidate','Candidate'),
    ])
    profile_status = models.CharField(max_length=100,null=True,choices=[
        ('Pending','Pending'),
        ('Accept','Accept'),
        ('Rejected','Rejected'),

    ])

    def __str__(self):
        return self.username
    