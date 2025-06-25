from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):

    role=[
        ('seeker',"Seeker"),
        ('recruiter',"Recruiter"),
    ]

    user_type=models.CharField(choices=role,max_length=100,null=True)