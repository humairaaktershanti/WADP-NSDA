from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUserModel(AbstractUser):
      phone = models.CharField(max_length=15, blank=True, null=True)
      user_type = models.CharField(max_length=10, choices=[('admin','Admin'),('employer', 'Employer'), ('candidate', 'Candidate')])


class PendingAccountModel(models.Model):
    username = models.CharField(max_length=150 )
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=[('employer', 'Employer'), ('candidate', 'Candidate')])
    pending_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accept', 'Accept'),('rejected', 'Rejected')], default='pending')
