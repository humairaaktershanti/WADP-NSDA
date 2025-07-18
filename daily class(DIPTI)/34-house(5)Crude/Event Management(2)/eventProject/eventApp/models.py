from django.db import models
from django.contrib.auth.models import AbstractUser


class customUserModel(AbstractUser):
    userType=models.CharField(max_length=100, choices=[
        ('EventManager', 'EventManager'),
        ('EventAttendee', 'EventAttendee'),
        
    ],null=True)

class eventModel(models.Model):
    user=models.ForeignKey(customUserModel, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=100,null=True)
    date=models.DateField(auto_now=True,null=True)
    location=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to='media/photo',null=True)

