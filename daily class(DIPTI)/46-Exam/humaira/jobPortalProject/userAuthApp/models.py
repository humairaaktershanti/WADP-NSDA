from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    userTypes = models.CharField(choices = [
        ('Admin','Admin'),
        ('Employer','Employer'),
        ('Candidate','Candidate')
    ], max_length = 100, null = True)
    phone = models.IntegerField(null = True)


class pendingAccountModel(models.Model):
    username=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)

    phone = models.IntegerField(null = True)
    userTypes = models.CharField(choices = [
             ('Employer','Employer'),
             ('Candidate','Candidate'),
                 ], max_length = 100, null = True)
    pendingStatus = models.CharField(choices = [
             ('Pending','Pending'),
             ('Accept','Accept'),
             ('Rejected','Rejected'),
    ], max_length = 100, null = True)

