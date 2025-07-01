from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    fullName = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='media/dp', null=True)
    address = models.TextField(null=True)
    createAt = models.DateTimeField(auto_now_add=True, null=True)
    citynName = models.CharField(max_length=100, null=True)
    bio = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)

class toDoModel(models.Model):
    user = models.ForeignKey(customUser,on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    status=models.CharField(choices=[
        ('pending','Pending'),
        ('inProgress','InProgress'),
        ('completed','Completed'),
    ],max_length=10, null=True)  
    created_at=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(auto_now_add=True,null=True)