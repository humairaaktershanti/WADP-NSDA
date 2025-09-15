from django.db import models
from django.contrib.auth.models import AbstractUser


class customUser(AbstractUser):
    USER_TYPES=(
        ('Admin' = 'Admin'),
        ('Employer' = 'Employer'),
        ('Candidate' = 'Candidate'),
    )user_types=models.CharField(choices=USER_TYPES,max_length=30,null=True)

    phone=models.CharField(max_length=15, null=True)


    def __str__(self):
        return self.username
    

class PendingAccountModel(models.Model):
    USER_TYPES=(
        ('Employer'= 'Employer'),
        ('Candidate'= 'Candidate'),
    )user_type = models.CharField(choices=USER_TYPES, max_length=30, null=True)

    PENDING_STATUS=(
        ('Pending'= 'Pending'),
        ('Accept'= 'Accept'),
        ('Rejected'= 'Rejected'),
    )pending_status=models.charField(choices=PENDING_STATUS, max_length=30, null=True)